"""Ticket Summarizer - RQ-1 happy-path slice.

Loads a Salesforce-shaped ticket fixture, flattens it into a chronological
thread, and asks the LLM for a structured summary containing the four fields
required by RQ-1: issue timeline, customer sentiment, prior commitments, and
unresolved questions.

Scope note: this slice covers RQ-1 / US-1 AC-1 only. PII redaction (RQ-2),
fallback (RQ-3), contradiction marking (AC-3), and audit logging are not
implemented here.
"""

import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from .llm import generate_text, get_model_name


def _utc_now_iso() -> str:
    """Default clock for audit timestamps. Injected over in tests."""
    return datetime.now(timezone.utc).isoformat()


def _new_request_id() -> str:
    """Default request-id source for audit correlation. Injected over in tests."""
    return str(uuid.uuid4())


# --- PII redaction (RQ-2 / US-1 AC-2) --------------------------------------
#
# In-scope PII per RQ-2: SSN, account numbers, date of birth. Each pattern maps
# to a [REDACTED-TYPE] token. Email/phone are intentionally excluded pending the
# open clarification in spec Section 6.
#
# Patterns are ordered so more specific shapes (SSN: 9 digits as 3-2-4) are tried
# before the broader account-number digit run, preventing an SSN being mistaken
# for an account number.
_PII_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("DOB", re.compile(r"\b\d{4}-\d{2}-\d{2}\b")),
    ("ACCOUNT", re.compile(r"\b\d{8,}\b")),
]


def redact_pii(text: str) -> tuple[str, list[str]]:
    """Replace in-scope PII with [REDACTED-TYPE] tokens.

    Returns the redacted text and the list of PII categories detected (each at
    most once), suitable for a PII-detected audit event. No identifiable
    fragment of a matched value is left behind (RQ-2 counter-example).
    """
    detected: list[str] = []
    for category, pattern in _PII_PATTERNS:
        if pattern.search(text):
            detected.append(category)
            text = pattern.sub(f"[REDACTED-{category}]", text)
    return text, detected


# --- Fixture loading -------------------------------------------------------

def load_fixture(path: str) -> dict[str, Any]:
    """Load a ticket fixture JSON and drop the non-Salesforce _fixture block.

    The _fixture key carries test metadata (expected summary, counter-example)
    that must never be fed to the model. Callers that need it should read the
    raw file separately via load_fixture_with_meta.
    """
    data = load_fixture_with_meta(path)
    data.pop("_fixture", None)
    return data


def load_fixture_with_meta(path: str) -> dict[str, Any]:
    """Load the full fixture JSON including the _fixture test-metadata block."""
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# --- Thread flattening -----------------------------------------------------

def flatten_and_redact(ticket: dict[str, Any]) -> tuple[str, list[str]]:
    """Render the thread with body PII redacted; report detected PII categories.

    Each line is tagged with author role so the model can distinguish customer
    messages, agent responses, and internal notes (the input types named in
    the spec). Events are sorted by their timestamp. Only message/comment
    bodies are redacted (RQ-2); the header and role/timestamp tags are left
    intact.
    """
    case = ticket.get("Case", {})
    contact = ticket.get("Contact", {})

    events: list[tuple[str, str]] = []
    detected: list[str] = []

    def redact_body(text: str) -> str:
        # RQ-2: redact in-scope PII from message/comment bodies only. Headers
        # and the role/timestamp tags are not customer-supplied PII (and the
        # ISO timestamps would otherwise trip the DOB pattern).
        clean, cats = redact_pii(text)
        for c in cats:
            if c not in detected:
                detected.append(c)
        return clean

    for msg in ticket.get("EmailMessages", {}).get("records", []):
        role = "CUSTOMER" if msg.get("Incoming") else "AGENT"
        who = msg.get("FromName", role)
        ts = msg.get("MessageDate", "")
        body = redact_body((msg.get("TextBody") or "").strip())
        events.append((ts, f"[{role}] {who} ({ts}): {body}"))

    for comment in ticket.get("CaseComments", {}).get("records", []):
        # Internal notes are agent-to-agent; tag distinctly so they are not
        # mistaken for customer sentiment.
        visibility = "PUBLIC NOTE" if comment.get("IsPublished") else "INTERNAL NOTE"
        ts = comment.get("CreatedDate", "")
        body = redact_body((comment.get("CommentBody") or "").strip())
        events.append((ts, f"[{visibility}] ({ts}): {body}"))

    events.sort(key=lambda e: e[0])
    transcript = "\n".join(line for _, line in events)

    header = (
        f"Ticket {case.get('CaseNumber', '?')} - {case.get('Subject', '')}\n"
        f"Customer: {contact.get('Name', 'unknown')}\n"
        f"Status: {case.get('Status', 'unknown')}\n"
    )
    return f"{header}\n{transcript}", detected


def flatten_thread(ticket: dict[str, Any]) -> str:
    """Render the redacted chronological transcript (string-only façade)."""
    thread, _ = flatten_and_redact(ticket)
    return thread


# --- Prompt + summary ------------------------------------------------------

SUMMARY_INSTRUCTIONS = """\
You are a customer-support handoff assistant. Read the ticket thread below and \
produce a structured summary for an agent taking over the case. Return ONLY a \
JSON object with exactly these keys:

  "timeline": a chronological list of strings (key events with dates)
  "sentiment": exactly one of "Positive", "Neutral", or "Negative"
  "prior_commitments": a list of strings (promises any agent made; include who \
and when if stated; empty list if none)
  "unresolved_questions": a list of strings (open issues, contradictions, \
unanswered questions; empty list if none)

Base every item strictly on the thread. Do not invent facts. If the customer \
reports something was not received but the record says it was done, treat that \
as unresolved, not resolved.

TICKET THREAD:
"""


def build_prompt_and_detect(ticket: dict[str, Any]) -> tuple[str, list[str]]:
    """Build the model prompt and report which PII categories were redacted.

    Redaction (RQ-2) happens in flatten_and_redact (body-only), before the
    thread reaches the model. The detected categories drive the PII-detected
    audit event (US-2 AC-2).
    """
    redacted_thread, detected = flatten_and_redact(ticket)
    return SUMMARY_INSTRUCTIONS + redacted_thread, detected


def build_prompt(ticket: dict[str, Any]) -> str:
    prompt, _ = build_prompt_and_detect(ticket)
    return prompt


def _extract_json(text: str) -> dict[str, Any]:
    """Pull the JSON object out of a model response that may be fenced."""
    text = text.strip()
    if text.startswith("```"):
        # strip ```json ... ``` fences
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON object found in model response: {text!r}")
    return json.loads(text[start : end + 1])


REQUIRED_KEYS = {"timeline", "sentiment", "prior_commitments", "unresolved_questions"}


FALLBACK_MESSAGE = "AI summary unavailable - manual review required"


class SummaryUnavailable(Exception):
    """Raised when the LLM gateway is unavailable or too slow (RQ-3).

    Carries the user-facing fallback message and an error code for the audit
    trail. The outage event is logged before this is raised, so the audit
    record exists regardless of how the caller handles the exception.
    """

    def __init__(self, error_code: str, message: str = FALLBACK_MESSAGE):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


def _no_audit(_event: dict[str, Any]) -> None:
    """Default audit sink: discard. Real deployments inject a logging sink."""


def summarize(
    ticket: dict[str, Any],
    _generate=generate_text,
    _audit=_no_audit,
    _clock=_utc_now_iso,
    _request_id=_new_request_id,
    _model=get_model_name,
) -> dict[str, Any]:
    """Generate the structured summary for a loaded ticket.

    All collaborators are injectable so tests can substitute doubles without a
    network call, a real logger, or non-deterministic time/ids:
      _generate   - the LLM gateway call
      _audit      - the audit-event sink
      _clock      - source of the audit timestamp
      _request_id - source of the audit correlation id
      _model      - source of the model version recorded in the audit trail

    When in-scope PII is redacted from the thread, a pii_detected audit event is
    emitted carrying the categories found plus timestamp, request id, and model
    version (RQ-2 / US-2 AC-2).
    """
    request_id = _request_id()

    def emit(event: str, **fields: Any) -> None:
        # Every audit event carries the same correlation metadata (US-2 AC-2):
        # timestamp, request id, and model version, plus event-specific fields.
        _audit(
            {
                "event": event,
                "timestamp": _clock(),
                "request_id": request_id,
                "model_version": _model(),
                **fields,
            }
        )

    prompt, detected = build_prompt_and_detect(ticket)
    if detected:
        emit("pii_detected", categories=detected)

    try:
        raw = _generate(prompt)
    except Exception as exc:  # gateway unavailable (RQ-3 / US-1 AC-4)
        error_code = type(exc).__name__
        emit("outage", fallback_triggered=True, error_code=error_code)
        raise SummaryUnavailable(error_code) from exc

    summary = _extract_json(raw)

    missing = REQUIRED_KEYS - summary.keys()
    if missing:
        raise ValueError(f"Summary missing required fields: {sorted(missing)}")
    return summary


def summarize_file(path: str, **collaborators) -> dict[str, Any]:
    """Load a fixture and summarize it. Injected collaborators (see summarize)
    are forwarded through, so tests can pass _generate/_audit/_clock/etc."""
    return summarize(load_fixture(path), **collaborators)

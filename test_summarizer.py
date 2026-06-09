"""Tests for the RQ-1 happy-path slice.

Derived from US-1 AC-1: given a ticket thread, a structured summary is produced
containing timeline, sentiment, prior commitments, and unresolved questions.

Offline tests use a fake generator seeded from each fixture's _fixture.
expected_summary block, so they assert the parsing/validation contract without
a network call. The live test (gated on an API key) exercises the real model.
"""

import json
import os

import pytest

import summarizer

FIXTURES = [
    "fixtures/ticket-48190-password-reset.json",
    "fixtures/ticket-48213-billing-dispute.json",
]


def _fake_generator_for(path):
    """Return a generate_text stand-in that emits the fixture's expected summary."""
    meta = summarizer.load_fixture_with_meta(path)["_fixture"]["expected_summary"]
    payload = {
        "timeline": (
            meta["timeline"] if isinstance(meta["timeline"], list) else [meta["timeline"]]
        ),
        "sentiment": meta["sentiment"],
        "prior_commitments": meta["prior_commitments"],
        "unresolved_questions": meta["unresolved"],
    }
    # Wrap in a code fence to also exercise _extract_json's fence handling.
    return lambda _prompt: "```json\n" + json.dumps(payload) + "\n```"


@pytest.mark.parametrize("path", FIXTURES)
def test_summary_has_required_fields(path):
    summary = summarizer.summarize_file(path, _generate=_fake_generator_for(path))
    assert summarizer.REQUIRED_KEYS <= summary.keys()
    assert summary["sentiment"] in {"Positive", "Neutral", "Negative"}
    assert isinstance(summary["timeline"], list)
    assert isinstance(summary["prior_commitments"], list)
    assert isinstance(summary["unresolved_questions"], list)


@pytest.mark.parametrize("path", FIXTURES)
def test_sentiment_matches_fixture_expectation(path):
    expected = summarizer.load_fixture_with_meta(path)["_fixture"]["expected_summary"]
    summary = summarizer.summarize_file(path, _generate=_fake_generator_for(path))
    assert summary["sentiment"] == expected["sentiment"]


def test_fixture_block_is_stripped_before_prompting():
    captured = {}

    def spy(prompt):
        captured["prompt"] = prompt
        return '{"timeline": [], "sentiment": "Neutral", "prior_commitments": [], "unresolved_questions": []}'

    summarizer.summarize_file(FIXTURES[0], _generate=spy)
    # Metadata that must never reach the model.
    assert "_fixture" not in captured["prompt"]
    assert "counter_example" not in captured["prompt"]
    assert "expected_summary" not in captured["prompt"]


def test_flatten_thread_tags_roles_and_orders_chronologically():
    ticket = summarizer.load_fixture("fixtures/ticket-48213-billing-dispute.json")
    thread = summarizer.flatten_thread(ticket)
    assert "[CUSTOMER]" in thread
    assert "[AGENT]" in thread
    assert "[INTERNAL NOTE]" in thread
    # First customer message precedes the escalation note.
    assert thread.index("second time this has happened") < thread.index("Escalating")


def test_missing_required_field_raises():
    bad = lambda _p: '{"sentiment": "Neutral", "timeline": []}'  # missing two keys
    with pytest.raises(ValueError, match="missing required fields"):
        summarizer.summarize_file(FIXTURES[0], _generate=bad)


# --- RQ-2 / US-1 AC-2: PII redaction ---------------------------------------
#
# Scope: SSN, account numbers, and date of birth are the in-scope PII named in
# RQ-2. Email and phone are deliberately NOT asserted here — the spec marks
# their status as an open clarification (spec Section 6).


def test_redact_pii_replaces_ssn_with_token():
    clean, detected = summarizer.redact_pii("Customer SSN is 123-45-6789, please verify.")
    assert "123-45-6789" not in clean
    assert "[REDACTED-SSN]" in clean
    assert "SSN" in detected


def test_redact_pii_leaves_no_identifiable_fragment():
    # Counter-example in RQ-2 forbids partial masking that leaves fragments.
    clean, _ = summarizer.redact_pii("SSN 123-45-6789 and acct 4567890123")
    assert "6789" not in clean
    assert "4567890123" not in clean


def test_redact_pii_reports_each_category_once():
    text = "SSN 123-45-6789, DOB 1990-04-12, account 4567890123"
    _, detected = summarizer.redact_pii(text)
    assert set(detected) == {"SSN", "DOB", "ACCOUNT"}


def test_redact_pii_clean_text_reports_nothing():
    clean, detected = summarizer.redact_pii("No sensitive data here.")
    assert detected == []
    assert clean == "No sensitive data here."


def _ticket_with_pii():
    """Minimal Salesforce-shaped ticket whose thread body carries in-scope PII."""
    return {
        "Case": {"CaseNumber": "00099999", "Subject": "Verify identity", "Status": "Open"},
        "Contact": {"Name": "Pat Doe"},
        "EmailMessages": {
            "records": [
                {
                    "Incoming": True,
                    "FromName": "Pat Doe",
                    "MessageDate": "2026-06-01T10:00:00.000+0000",
                    "TextBody": "My SSN is 123-45-6789 and my account is 4567890123.",
                }
            ]
        },
        "CaseComments": {"records": []},
    }


def test_prompt_contains_no_raw_in_scope_pii():
    # RQ-2: redaction must happen before the model sees the thread.
    prompt = summarizer.build_prompt(_ticket_with_pii())
    assert "123-45-6789" not in prompt
    assert "4567890123" not in prompt
    assert "[REDACTED-SSN]" in prompt
    assert "[REDACTED-ACCOUNT]" in prompt


# --- RQ-2 / US-2 AC-2: PII-detected audit event ----------------------------
#
# The audit sink is injected (IoC): tests pass a list-appending double rather
# than patching a global logger.

_EMPTY_SUMMARY = (
    '{"timeline": [], "sentiment": "Neutral", '
    '"prior_commitments": [], "unresolved_questions": []}'
)


def test_pii_detected_event_logged_with_categories():
    events = []
    summarizer.summarize(
        _ticket_with_pii(),
        _generate=lambda _p: _EMPTY_SUMMARY,
        _audit=events.append,
    )
    pii_events = [e for e in events if e["event"] == "pii_detected"]
    assert len(pii_events) == 1
    assert set(pii_events[0]["categories"]) == {"SSN", "ACCOUNT"}


def test_no_pii_means_no_pii_event():
    events = []
    summarizer.summarize_file(
        FIXTURES[0],  # password-reset fixture: no in-scope PII in the thread
        _generate=lambda _p: _EMPTY_SUMMARY,
        _audit=events.append,
    )
    assert [e for e in events if e["event"] == "pii_detected"] == []


def test_audit_event_carries_timestamp_request_id_and_model():
    # US-2 AC-2: audit records include timestamp, request identifier, and model
    # version. All three are injected (IoC) so the assertion is deterministic --
    # no env vars, no clock patching.
    events = []
    summarizer.summarize(
        _ticket_with_pii(),
        _generate=lambda _p: _EMPTY_SUMMARY,
        _audit=events.append,
        _clock=lambda: "2026-06-09T12:00:00Z",
        _request_id=lambda: "req-abc-123",
        _model=lambda: "gemini-test-1.0",
    )
    event = next(e for e in events if e["event"] == "pii_detected")
    assert event["timestamp"] == "2026-06-09T12:00:00Z"
    assert event["request_id"] == "req-abc-123"
    assert event["model_version"] == "gemini-test-1.0"


def test_redaction_spares_header_and_timestamps():
    # Case number and message timestamps are not customer-supplied PII; only
    # message/comment bodies are redacted. (Body-only redaction scope.)
    thread = summarizer.flatten_thread(_ticket_with_pii())
    assert "00099999" in thread          # case number survives
    assert "2026-06-01" in thread        # event timestamp survives
    assert "123-45-6789" not in thread   # body SSN is gone
    assert "[REDACTED-SSN]" in thread


# --- RQ-3 / US-1 AC-4: fallback when the LLM gateway is unavailable ---------
#
# On gateway failure, summarize raises a typed SummaryUnavailable carrying the
# fallback message and an error code, and logs an outage event FIRST so the
# audit trail is guaranteed regardless of how the caller handles the exception.

FALLBACK_MESSAGE = "AI summary unavailable - manual review required"


def test_gateway_failure_raises_summary_unavailable():
    def boom(_prompt):
        raise ConnectionError("gateway 503")

    with pytest.raises(summarizer.SummaryUnavailable) as exc_info:
        summarizer.summarize(_ticket_with_pii(), _generate=boom)
    assert exc_info.value.message == FALLBACK_MESSAGE


def test_gateway_failure_logs_outage_event():
    events = []

    def boom(_prompt):
        raise ConnectionError("gateway 503")

    with pytest.raises(summarizer.SummaryUnavailable):
        summarizer.summarize(
            _ticket_with_pii(),
            _generate=boom,
            _audit=events.append,
            _clock=lambda: "2026-06-09T12:00:00Z",
            _request_id=lambda: "req-outage-1",
        )
    outage = next(e for e in events if e["event"] == "outage")
    assert outage["fallback_triggered"] is True
    assert outage["error_code"]              # an error code is recorded
    assert outage["timestamp"] == "2026-06-09T12:00:00Z"
    assert outage["request_id"] == "req-outage-1"


# This is the ONLY test that calls the real Gemini API (it omits _generate=,
# so summarize_file falls back to llm.generate_text). It is opt-in: it runs
# only when RUN_LIVE=1 is explicitly set AND a key is available. A stray key in
# the shell environment alone will NOT trigger a billed call.
@pytest.mark.skipif(
    os.getenv("RUN_LIVE") != "1",
    reason="live model test is opt-in; set RUN_LIVE=1 to enable",
)
@pytest.mark.parametrize("path", FIXTURES)
def test_live_summary_against_real_model(path):
    """End-to-end against the real gateway. Asserts the contract and that the
    expected sentiment is produced for these unambiguous fixtures."""
    from dotenv import load_dotenv

    load_dotenv()
    expected = summarizer.load_fixture_with_meta(path)["_fixture"]["expected_summary"]
    summary = summarizer.summarize_file(path)
    assert summarizer.REQUIRED_KEYS <= summary.keys()
    assert summary["sentiment"] == expected["sentiment"]

# AGENTS.md

Guidance for AI agents working in this repo. Setup and run instructions live in
the [README](README.md) — this file covers the conventions that aren't obvious
from the code.

## What this is

The RQ-1 happy-path slice of a customer support ticket summarizer: load a
Salesforce-shaped ticket, flatten it to a chronological thread, and ask an LLM
for a four-field structured summary (timeline, sentiment, prior commitments,
unresolved questions). RQ-2 (PII redaction + audit) is partially in; RQ-3
(fallback) is partial. Spec lives in [docs/](docs/).

## Layout gotcha: the package re-exports its API

- Production code is the package `src/summarizer/`. The core module is
  `core.py` (it can't be named `summarizer.py` — that's the package).
- The public API is re-exported through `src/summarizer/__init__.py`. Tests and
  callers use `import summarizer; summarizer.summarize(...)`.
- **When you add a public function to `core.py`, you must also add it to the
  imports and `__all__` in `__init__.py`** — otherwise `summarizer.foo` raises
  `AttributeError` even though the function exists.
- `src/` is a real package (editable-installed via `pyproject.toml`), not a flat
  source dir. There is no `requirements.txt`; dependencies live in
  `pyproject.toml`.

## Convention: dependency injection, not mocks (IoC)

Side effects are passed in as keyword arguments with sensible defaults, so tests
substitute doubles instead of monkeypatching globals. The seams on
`summarize` / `summarize_file` are:

| Param | Injects | Default |
| --- | --- | --- |
| `_generate` | the LLM call | `llm.generate_text` |
| `_audit` | the audit-event sink | `_no_audit` (no-op) |
| `_clock` | timestamp source | UTC now |
| `_request_id` | correlation id | a fresh uuid |
| `_model` | model-name source | `llm.get_model_name` |

**When you add a new side effect (network, clock, randomness, file/DB I/O),
expose it as an injectable parameter the same way.** Don't reach for
`unittest.mock` or monkeypatching — the suite is deliberately mock-free and
deterministic.

## Convention: TDD, sliced by spec acceptance criteria

- Test-first, one RQ / user-story acceptance criterion at a time.
- Tests cite the spec AC they cover (see the comments in
  `tests/test_summarizer.py`). Keep that traceability when adding tests.

## Safety: live API calls are opt-in and must stay that way

- The default `pytest` run is fully offline — every test injects a fake
  `_generate`, so no key and no network are needed.
- Exactly one test hits the real Gemini API, gated behind `RUN_LIVE=1`. A stray
  key in the environment alone will **not** trigger a billed call.
- Do not add un-gated network calls to the default suite, and do not weaken the
  `RUN_LIVE` guard.

## Safety: PII and the spec constraints

- GLBA constraint: do not log or persist PII beyond the active session. PII
  detection emits an audit event (categories only), not the raw values.
- Fixtures carry a `_fixture` metadata block (expected outputs for tests). It
  must be stripped before any ticket is sent to the model — see how the web
  handler does `ticket.pop("_fixture", None)`. Preserve that anywhere new that
  feeds tickets to the LLM.

## LLM backend: provider switch in llm.py

- `src/summarizer/llm.py` dispatches on the `LLM_PROVIDER` env var. Two backends
  are wired:
  - **`gemini`** (default) — `google-genai` SDK. Config: `GEMINI_API_KEY` /
    `GOOGLE_API_KEY`, optional `GEMINI_MODEL`.
  - **`ollama`** — a local Ollama server over HTTP, stdlib only (no extra deps).
    Config: `OLLAMA_MODEL` / `OLLAMA_HOST` / `OLLAMA_PORT`.
- `generate_text(prompt)` is the single public entry point and the default
  `_generate` collaborator. Core and the tests only ever see `generate_text`, so
  they're backend-agnostic. **To add a backend: add a `_generate_*` function and
  a branch in `generate_text` — don't thread a provider arg through core.**
- Connectivity is exercised through the real backend now; there's no separate
  probe script. To smoke-test Ollama, run any summary with `LLM_PROVIDER=ollama`.

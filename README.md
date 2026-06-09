# Customer Support Ticket Summarizer

Generates a structured handoff summary for a customer support ticket so an agent
picking up the case can get oriented in seconds instead of reading the whole
thread. Each summary contains four fields:

- **Issue timeline** — what happened, in order
- **Customer sentiment** — Positive / Neutral / Negative
- **Prior commitments** — what was promised to the customer
- **Unresolved questions** — what still needs an answer

The goal (per the project spec) is to cut average handoff prep time from ~12
minutes to under 3. This repo is the **RQ-1 happy-path slice**: load a
Salesforce-shaped ticket, flatten it into a chronological thread, and ask the
LLM for the structured summary. PII redaction, fallback handling, and audit
logging are tracked separately and not all implemented here.

> The intended production delivery is inside Salesforce Service Cloud (no new
> UI). The CLI and web UI in this repo are developer/demo harnesses for local
> testing.

## Requirements

- Python ≥ 3.11
- An LLM backend — either a Gemini API key (default) or a local Ollama server.
  See [Choosing a backend](#choosing-a-backend).

## Setup

```bash
# create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install the package (editable) plus the test tooling
pip install -e . --group dev
```

> On Windows, activate the virtual environment with `.venv\Scripts\activate`
> instead of `source .venv/bin/activate`.

Then configure a backend. Copy the example env file and fill it in:

```bash
cp .env.example .env
# edit .env: set GEMINI_API_KEY=...   (or LLM_PROVIDER=ollama, see below)
```

### Choosing a backend

Set `LLM_PROVIDER` to pick the LLM (defaults to `gemini`).

**Gemini** (`LLM_PROVIDER=gemini`) — set at least one API key:

| Variable | Required | Purpose |
| --- | --- | --- |
| `GEMINI_API_KEY` | yes* | Gemini API key (preferred) |
| `GOOGLE_API_KEY` | yes* | Alternative key name some Google SDKs accept |
| `GEMINI_MODEL` | no | Override the model (default `gemini-3.5-flash`) |

\* Set at least one of `GEMINI_API_KEY` / `GOOGLE_API_KEY`.

**Ollama** (`LLM_PROVIDER=ollama`) — runs against a local
[Ollama](https://ollama.com) server; no API key needed. Pull a model first
(e.g. `ollama pull qwen3.5`):

| Variable | Required | Purpose |
| --- | --- | --- |
| `OLLAMA_MODEL` | no | Model to use (default `qwen3.5`) |
| `OLLAMA_HOST` | no | Server host (default `localhost`) |
| `OLLAMA_PORT` | no | Server port (default `11434`) |

## Running

Installing the package exposes two console commands.

### CLI

```bash
summarizer tests/fixtures/ticket-48190-password-reset.json
```

Add `--json` to print the raw structured summary instead of the formatted view:

```bash
summarizer tests/fixtures/ticket-48190-password-reset.json --json
```

### Web demo UI

```bash
summarizer-web
# then open http://localhost:8000
```

Paste ticket JSON into the textarea and submit to see the rendered summary.

## Tests

```bash
pytest
```

Offline tests use a fake generator seeded from each fixture, so the suite runs
without a network call or API key. One end-to-end test hits the real Gemini API
and is opt-in — it runs only when explicitly enabled:

```bash
RUN_LIVE=1 pytest
```

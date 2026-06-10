"""Minimal dev/demo web UI for the Ticket Summarizer.

Zero dependencies beyond the stdlib (http.server). GET serves a form with a
textarea for ticket JSON; POST runs summarize() and renders the four-field
summary as formatted HTML.

NOTE: this is a developer/demo harness only. The spec's intended delivery is
inside Salesforce Service Cloud (no new UI), so this is for local testing.

Run:  summarizer-web      then open http://localhost:8000
"""

import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from string import Template
from urllib.parse import parse_qs

from dotenv import load_dotenv

from .core import summarize

PORT = 8000

# Cap POST bodies so a runaway/oversized paste can't be read into memory
# unbounded. Generous for ticket JSON; this is a localhost dev tool, not a
# tuned production limit.
MAX_BODY_BYTES = 2 * 1024 * 1024  # 2 MB

_TEMPLATES = files(__package__).joinpath("templates")
_STYLES = _TEMPLATES.joinpath("styles.css").read_text("utf-8")
_INDEX = _TEMPLATES.joinpath("index.html").read_text("utf-8")
# Inline the stylesheet once at import; $ticket/$result stay for per-request render.
PAGE = Template(Template(_INDEX).safe_substitute(styles=_STYLES))


# Bound how much model output we render: cap list length and per-item size so a
# malformed/pathological response can't blow up the page. Generous vs. any real
# handoff summary.
_MAX_ITEMS = 200
_MAX_ITEM_CHARS = 2000


def _render_summary(summary: dict) -> str:
    def items(key: str) -> str:
        vals = summary.get(key) or []
        if not isinstance(vals, list):
            vals = [vals]
        if not vals:
            return '<p class="muted">(none)</p>'
        shown = vals[:_MAX_ITEMS]
        lis = "".join(
            f"<li>{html.escape(str(v)[:_MAX_ITEM_CHARS])}</li>" for v in shown
        )
        if len(vals) > _MAX_ITEMS:
            lis += f'<li class="muted">(+{len(vals) - _MAX_ITEMS} more truncated)</li>'
        return f"<ul>{lis}</ul>"

    sentiment = html.escape(str(summary.get("sentiment", "Unknown")))
    cls = sentiment if sentiment in ("Positive", "Neutral", "Negative") else "Neutral"
    return f"""
<div class="summary">
  <section>
    <h2>Sentiment</h2>
    <span class="sentiment {cls}">{sentiment}</span>
  </section>
  <section><h2>Timeline</h2>{items("timeline")}</section>
  <section><h2>Prior commitments</h2>{items("prior_commitments")}</section>
  <section><h2>Unresolved questions</h2>{items("unresolved_questions")}</section>
</div>
"""


def _render_error(message: str) -> str:
    return f'<div class="err">{html.escape(message)}</div>'


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: str, status: int = 200) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self._send(_render_error("Not found"), status=404)
            return
        self._send(PAGE.substitute(ticket="", result=""))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > MAX_BODY_BYTES:
            self._send(
                _render_error("Request too large (max 2 MB)."), status=413
            )
            return
        raw = self.rfile.read(length).decode("utf-8")
        fields = parse_qs(raw, keep_blank_values=True)
        ticket_text = (fields.get("ticket", [""])[0]).strip()

        result, echo = "", ticket_text
        try:
            if not ticket_text:
                raise ValueError("Please paste ticket JSON.")
            ticket = json.loads(ticket_text)
            ticket.pop("_fixture", None)  # never feed test metadata to the model
            summary = summarize(ticket)
            result = _render_summary(summary)
        except json.JSONDecodeError as exc:
            result = _render_error(f"Invalid JSON: {exc}")
        except (ValueError, KeyError) as exc:
            result = _render_error(f"Could not summarize: {exc}")
        except Exception:  # noqa: BLE001 - dev tool: don't leak internals to page
            # The detail is printed to the console; the page gets a generic
            # message so model/gateway internals aren't exposed in the response.
            import traceback

            traceback.print_exc()
            result = _render_error("Summarization failed - see server console.")

        self._send(PAGE.substitute(ticket=html.escape(echo), result=result))

    def log_message(self, *args, **kwargs):  
        # quieter console
        pass


def main() -> int:
    load_dotenv()
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Ticket Summarizer dev UI -> http://localhost:{PORT}  (Ctrl-C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

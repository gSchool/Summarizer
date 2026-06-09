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
from urllib.parse import parse_qs

from dotenv import load_dotenv

from .core import summarize

PORT = 8000

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ticket Summarizer</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 15px/1.5 system-ui, sans-serif; max-width: 820px;
         margin: 2rem auto; padding: 0 1rem; }}
  h1 {{ font-size: 1.4rem; }}
  textarea {{ width: 100%; height: 16rem; font: 13px/1.4 ui-monospace, monospace;
             padding: .6rem; box-sizing: border-box; }}
  button {{ margin-top: .6rem; padding: .5rem 1.1rem; font-size: 1rem;
           cursor: pointer; }}
  .err {{ background: #fde8e8; color: #9b1c1c; padding: .8rem 1rem;
         border-radius: 6px; margin: 1rem 0; }}
  .summary {{ margin-top: 1.5rem; }}
  .sentiment {{ display: inline-block; padding: .2rem .7rem; border-radius: 999px;
               font-weight: 600; }}
  .Positive {{ background: #def7ec; color: #03543f; }}
  .Neutral  {{ background: #e5e7eb; color: #374151; }}
  .Negative {{ background: #fde8e8; color: #9b1c1c; }}
  section {{ margin-top: 1.2rem; }}
  section h2 {{ font-size: 1rem; margin-bottom: .3rem; }}
  ul {{ margin: 0; padding-left: 1.2rem; }}
  .muted {{ color: #6b7280; }}
  textarea.drag {{ outline: 2px dashed #6b7280; outline-offset: 2px; }}
</style>
</head>
<body>
<h1>Ticket Summarizer <span class="muted">(dev harness)</span></h1>
<form method="post">
  <label for="ticket">Paste ticket fixture JSON <span class="muted">(or drop a .json file)</span>:</label>
  <textarea id="ticket" name="ticket" placeholder='{{"Case": {{...}}, "EmailMessages": {{...}}}}'>{ticket}</textarea>
  <button type="submit">Summarize</button>
</form>
{result}
<script>
  const ta = document.getElementById("ticket");
  // Prevent the browser from navigating to a dropped file anywhere on the page.
  ["dragover", "drop"].forEach(ev =>
    window.addEventListener(ev, e => e.preventDefault()));
  ["dragenter", "dragover"].forEach(ev =>
    ta.addEventListener(ev, () => ta.classList.add("drag")));
  ["dragleave", "drop"].forEach(ev =>
    ta.addEventListener(ev, () => ta.classList.remove("drag")));
  ta.addEventListener("drop", e => {{
    const file = e.dataTransfer.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {{ ta.value = reader.result; }};
    reader.readAsText(file);
  }});
</script>
</body>
</html>
"""


def _render_summary(summary: dict) -> str:
    def items(key: str) -> str:
        vals = summary.get(key) or []
        if not vals:
            return '<p class="muted">(none)</p>'
        lis = "".join(f"<li>{html.escape(str(v))}</li>" for v in vals)
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
        self._send(PAGE.format(ticket="", result=""))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
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
        except Exception as exc:  # surface model/network errors to the page
            result = _render_error(f"Summarization failed: {exc}")

        self._send(PAGE.format(ticket=html.escape(echo), result=result))

    def log_message(self, *args):  # quieter console
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

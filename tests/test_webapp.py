"""Smoke tests for the dev/demo web UI template wiring.

These cover the packaged template loading and the substitute/escape contract
without standing up a server or touching the model.
"""

from summarizer import webapp


def test_page_template_loads_and_substitutes():
    out = webapp.PAGE.substitute(ticket="", result="")
    assert "<title>Ticket Summarizer</title>" in out
    assert "FileReader" in out  # the drag-and-drop script survived the move
    assert ".sentiment {" in out  # styles.css was inlined at load
    # No leftover placeholders after substitution.
    assert "$ticket" not in out
    assert "$result" not in out


def test_page_substitutes_ticket_and_result():
    out = webapp.PAGE.substitute(ticket="HELLO_TICKET", result="HELLO_RESULT")
    assert "HELLO_TICKET" in out
    assert "HELLO_RESULT" in out


def test_render_summary_marks_sentiment_class():
    summary = {
        "sentiment": "Negative",
        "timeline": ["t1"],
        "prior_commitments": [],
        "unresolved_questions": ["q1"],
    }
    html = webapp._render_summary(summary)
    assert 'class="sentiment Negative"' in html
    assert "<li>t1</li>" in html
    assert '<p class="muted">(none)</p>' in html  # empty prior_commitments


def test_render_error_escapes_html():
    out = webapp._render_error("<script>boom</script>")
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


def test_render_summary_caps_list_length():
    summary = {
        "sentiment": "Neutral",
        "timeline": [f"event {i}" for i in range(webapp._MAX_ITEMS + 50)],
        "prior_commitments": [],
        "unresolved_questions": [],
    }
    html = webapp._render_summary(summary)
    assert html.count("<li>") == webapp._MAX_ITEMS
    assert "50 more truncated" in html


def test_render_summary_caps_item_length():
    summary = {
        "sentiment": "Neutral",
        "timeline": ["x" * (webapp._MAX_ITEM_CHARS + 100)],
        "prior_commitments": [],
        "unresolved_questions": [],
    }
    html = webapp._render_summary(summary)
    assert "x" * webapp._MAX_ITEM_CHARS in html
    assert "x" * (webapp._MAX_ITEM_CHARS + 1) not in html


def test_render_summary_tolerates_non_list_field():
    # A model returning a scalar instead of a list must not crash the render.
    summary = {
        "sentiment": "Neutral",
        "timeline": "single string not a list",
        "prior_commitments": [],
        "unresolved_questions": [],
    }
    html = webapp._render_summary(summary)
    assert "<li>single string not a list</li>" in html

"""Ticket Summarizer package.

Public API is re-exported from .core so callers (and tests) can use
`import summarizer; summarizer.summarize(...)` against a stable surface.
"""

from .core import (
    REQUIRED_KEYS,
    SummaryUnavailable,
    build_prompt,
    flatten_thread,
    load_fixture,
    load_fixture_with_meta,
    redact_pii,
    summarize,
    summarize_file,
)

__all__ = [
    "REQUIRED_KEYS",
    "SummaryUnavailable",
    "build_prompt",
    "flatten_thread",
    "load_fixture",
    "load_fixture_with_meta",
    "redact_pii",
    "summarize",
    "summarize_file",
]

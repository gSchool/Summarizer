"""Ticket Summarizer package.

The public API is the orchestration surface a caller actually uses: summarize
a ticket (or a fixture file), the fallback exception they must handle, and the
fixture loaders. Pure helpers (redact_pii, extract_json, build_prompt,
flatten_thread) are deliberately NOT re-exported — they are units with their
own contracts, unit-tested via `summarizer.core`, but we make no public promise
about them until a real caller needs one. See the conventions memory for the
"promote only on demand" stance.
"""

from .core import (
    REQUIRED_KEYS,
    SummaryUnavailable,
    load_fixture,
    load_fixture_with_meta,
    summarize,
    summarize_file,
)

__all__ = [
    "REQUIRED_KEYS",
    "SummaryUnavailable",
    "load_fixture",
    "load_fixture_with_meta",
    "summarize",
    "summarize_file",
]

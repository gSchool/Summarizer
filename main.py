import argparse
import json
import sys

from dotenv import load_dotenv

from summarizer import summarize_file


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Generate a structured handoff summary for a ticket fixture (RQ-1)."
    )
    parser.add_argument("fixture", help="Path to a ticket fixture JSON file.")
    parser.add_argument(
        "--json", action="store_true", help="Print the summary as raw JSON."
    )
    args = parser.parse_args()

    try:
        summary = summarize_file(args.fixture)
    except (ValueError, FileNotFoundError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        _print_human(summary)
    return 0


def _print_human(summary: dict) -> None:
    print(f"Sentiment: {summary['sentiment']}\n")
    print("Timeline:")
    for item in summary["timeline"]:
        print(f"  - {item}")
    print("\nPrior commitments:")
    for item in summary["prior_commitments"] or ["(none)"]:
        print(f"  - {item}")
    print("\nUnresolved questions:")
    for item in summary["unresolved_questions"] or ["(none)"]:
        print(f"  - {item}")


if __name__ == "__main__":
    raise SystemExit(main())

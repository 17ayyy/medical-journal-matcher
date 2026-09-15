from __future__ import annotations

import argparse
import json
from pathlib import Path

from medical_journal_matcher.scoring import calculate_match_score


def main() -> None:
    parser = argparse.ArgumentParser(description="Score versioned atomic candidate features.")
    parser.add_argument("input", type=Path, help="JSON with 'features' and 'weights' objects")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = calculate_match_score(payload["features"], payload["weights"])
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

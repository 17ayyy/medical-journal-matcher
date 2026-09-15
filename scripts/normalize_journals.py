from __future__ import annotations

import argparse
import json
from pathlib import Path

from medical_journal_matcher.normalization import normalize_issn


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize ISSN fields in journal JSON records.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    records = json.loads(args.input.read_text(encoding="utf-8"))
    for record in records:
        for field in ("issn_l", "pissn", "eissn"):
            if record.get(field):
                record[field] = normalize_issn(record[field])
    args.output.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

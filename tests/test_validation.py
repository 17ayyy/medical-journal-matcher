import json
from pathlib import Path

from medical_journal_matcher.validation import validate_output


def test_schema_rejects_missing_top_level_fields() -> None:
    schema = Path("references/output-schema.json")
    errors = validate_output({"schema_version": "1.0.0"}, schema)
    assert errors


def test_schema_is_valid_json() -> None:
    json.loads(Path("references/output-schema.json").read_text(encoding="utf-8"))


def test_semantics_reject_nonpassing_formal_gate() -> None:
    schema = Path("references/output-schema.json")
    instance = {
        "schema_version": "1.0.0",
        "recommendations": {
            "sprint": [
                {
                    "strategy_tier": "SPRINT",
                    "gates": [{"gate_key": "jcr", "status": "UNVERIFIED"}],
                    "score": {"final_match_score": 90.0, "score_coverage": 1.0},
                    "confidence": {"level": "HIGH"},
                    "similar_articles": [],
                }
            ],
            "priority": [],
            "relatively_safe": [],
        },
    }
    errors = validate_output(instance, schema)
    assert any("non-passing gates" in error for error in errors)

import json
from copy import deepcopy
from pathlib import Path

from medical_journal_matcher.validation import validate_output
from tests.factories import candidate, recommendation, valid_output

SCHEMA = Path("references/output-schema.json")


def test_valid_public_output_with_no_formal_recommendations() -> None:
    assert validate_output(valid_output(), SCHEMA) == []


def test_schema_rejects_missing_top_level_fields() -> None:
    errors = validate_output({"schema_version": "1.0.0"}, SCHEMA)
    assert errors


def test_schema_is_valid_json() -> None:
    json.loads(SCHEMA.read_text(encoding="utf-8"))


def test_semantics_reject_nonpassing_formal_gate() -> None:
    instance = valid_output(jcr_data_mode="USER_JCR_IMPORT")
    item = recommendation()
    item["gates"][0]["status"] = "UNVERIFIED"
    instance["recommendations"]["priority"].append(item)

    errors = validate_output(instance, SCHEMA)
    assert any("non-passing gates" in error for error in errors)


def test_public_mode_rejects_formal_recommendations() -> None:
    instance = valid_output()
    instance["recommendations"]["priority"].append(recommendation())

    errors = validate_output(instance, SCHEMA)
    assert any("PUBLIC JCR mode" in error for error in errors)


def test_licensed_mode_accepts_valid_formal_recommendation() -> None:
    instance = valid_output(jcr_data_mode="USER_JCR_IMPORT")
    instance["recommendations"]["priority"].append(recommendation())
    assert validate_output(instance, SCHEMA) == []


def test_formal_article_must_be_unique_and_inside_window() -> None:
    instance = valid_output(jcr_data_mode="USER_JCR_IMPORT")
    item = recommendation()
    duplicate = deepcopy(item["similar_articles"][0])
    duplicate["publication_date"] = "2023-09-15"
    item["similar_articles"].append(duplicate)
    instance["recommendations"]["priority"].append(item)

    errors = validate_output(instance, SCHEMA)
    assert any("duplicated" in error for error in errors)
    assert any("outside the evidence window" in error for error in errors)


def test_unverified_bucket_requires_unverified_without_fail() -> None:
    all_pass = candidate()
    failed = candidate(gate_status="FAIL")
    instance = valid_output()
    instance["unverified_candidates"] = [all_pass, failed]

    errors = validate_output(instance, SCHEMA)
    assert any("must have at least one unverified gate" in error for error in errors)
    assert any("belongs in exclusions" in error for error in errors)


def test_source_fact_references_must_resolve() -> None:
    instance = valid_output()
    item = candidate(gate_status="UNVERIFIED")
    item["journal"]["source_fact_ids"] = ["missing-source"]
    instance["unverified_candidates"].append(item)

    errors = validate_output(instance, SCHEMA)
    assert any("unknown source_fact_id 'missing-source'" in error for error in errors)


def test_complete_fixed_disclaimer_is_required() -> None:
    instance = valid_output()
    instance["disclaimers"] = ["不是录用保证。"]

    errors = validate_output(instance, SCHEMA)
    assert any("complete fixed disclaimer" in error for error in errors)

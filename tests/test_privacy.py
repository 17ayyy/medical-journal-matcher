import pytest

from medical_journal_matcher.privacy import build_outbound_query


def test_query_builder_rejects_manuscript_text_fields() -> None:
    with pytest.raises(ValueError, match="non-allowlisted"):
        build_outbound_query({"topics": ["sepsis"], "abstract": "unpublished text"})


def test_query_builder_keeps_only_structured_allowlisted_values() -> None:
    assert build_outbound_query(
        {
            "topics": ["sepsis", "ultrasound"],
            "study_designs": ["DIAGNOSTIC_ACCURACY"],
        }
    ) == {
        "topics": ["sepsis", "ultrasound"],
        "study_designs": ["DIAGNOSTIC_ACCURACY"],
    }

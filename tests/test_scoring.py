import pytest

from medical_journal_matcher.scoring import calculate_match_score, score_confidence


def test_null_scores_reduce_coverage_without_counting_as_zero() -> None:
    weights = {"scope": 60.0, "evidence": 40.0}
    result = calculate_match_score({"scope": 0.8, "evidence": None}, weights)
    assert result.final_match_score == 80.0
    assert result.score_coverage == 0.6


def test_nonpassing_gate_forces_low_confidence() -> None:
    weights = {"a": 0.5, "b": 0.5}
    score, level = score_confidence(
        {"a": 1.0, "b": 1.0},
        weights,
        has_nonpassing_enabled_gate=True,
    )
    assert score == 1.0
    assert level == "LOW"


def test_weights_must_sum_to_versioned_total() -> None:
    with pytest.raises(ValueError, match="sum to 100"):
        calculate_match_score({"scope": 1.0}, {"scope": 99.0})

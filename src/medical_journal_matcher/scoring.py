from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class MatchScore:
    final_match_score: float | None
    score_coverage: float
    assessed_weight: float
    raw_weighted_points: float


def calculate_match_score(
    feature_scores: Mapping[str, float | None],
    weights: Mapping[str, float],
) -> MatchScore:
    """Calculate the PRD's null-aware score and coverage deterministically."""
    unknown = set(feature_scores) - set(weights)
    if unknown:
        raise KeyError(f"Unknown scoring features: {', '.join(sorted(unknown))}")
    if not weights or any(weight < 0 for weight in weights.values()):
        raise ValueError("Weights must be non-empty and non-negative")
    if round(sum(weights.values()), 8) != 100.0:
        raise ValueError("Versioned weights must sum to 100")

    assessed_weight = 0.0
    raw_weighted_points = 0.0
    for key, score in feature_scores.items():
        if score is None:
            continue
        if not 0 <= score <= 1:
            raise ValueError(f"Feature {key!r} must be between 0 and 1 or null")
        weight = weights[key]
        assessed_weight += weight
        raw_weighted_points += weight * score

    coverage = assessed_weight / 100.0
    final = None if assessed_weight == 0 else raw_weighted_points / assessed_weight * 100.0
    return MatchScore(
        final_match_score=None if final is None else round(final, 1),
        score_coverage=round(coverage, 4),
        assessed_weight=round(assessed_weight, 4),
        raw_weighted_points=round(raw_weighted_points, 4),
    )


def score_confidence(
    components: Mapping[str, float],
    weights: Mapping[str, float],
    *,
    has_nonpassing_enabled_gate: bool = False,
) -> tuple[float, str]:
    if set(components) != set(weights):
        raise ValueError("Confidence components and weights must have identical keys")
    if round(sum(weights.values()), 8) != 1.0:
        raise ValueError("Confidence weights must sum to 1")
    if any(not 0 <= value <= 1 for value in components.values()):
        raise ValueError("Confidence components must be between 0 and 1")

    score = round(sum(components[key] * weights[key] for key in weights), 2)
    if has_nonpassing_enabled_gate:
        return score, "LOW"
    if score >= 0.80 and min(components.values()) >= 0.50:
        return score, "HIGH"
    if score >= 0.60:
        return score, "MEDIUM"
    return score, "LOW"

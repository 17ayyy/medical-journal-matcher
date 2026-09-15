from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .normalization import is_doi_syntax_valid

FORMAL_TIERS = {
    "sprint": "SPRINT",
    "priority": "PRIORITY",
    "relatively_safe": "RELATIVELY_SAFE",
}
PASSING_CONFIDENCE = {"HIGH", "MEDIUM"}
PASSING_INTEGRITY = {"CLEAR", "CORRECTED"}


def validate_output(instance: dict[str, Any], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
    messages = [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in errors
    ]
    messages.extend(_validate_formal_recommendations(instance))
    return messages


def _validate_formal_recommendations(instance: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    recommendations = instance.get("recommendations")
    if not isinstance(recommendations, dict):
        return messages

    for bucket, expected_tier in FORMAL_TIERS.items():
        items = recommendations.get(bucket, [])
        if not isinstance(items, list):
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            path = f"recommendations/{bucket}/{index}"
            if item.get("strategy_tier") != expected_tier:
                messages.append(f"{path}: strategy_tier must be {expected_tier}")

            gates = item.get("gates", [])
            nonpassing = [
                gate.get("gate_key", "<unknown>")
                for gate in gates
                if isinstance(gate, dict) and gate.get("status") not in {"PASS", "NOT_APPLICABLE"}
            ]
            if nonpassing:
                messages.append(f"{path}: formal recommendation has non-passing gates {nonpassing}")

            score = item.get("score", {})
            if isinstance(score, dict):
                final = score.get("final_match_score")
                coverage = score.get("score_coverage")
                if not isinstance(final, int | float) or final < 65.0:
                    messages.append(f"{path}: final_match_score must be at least 65.0")
                if not isinstance(coverage, int | float) or coverage < 0.80:
                    messages.append(f"{path}: score_coverage must be at least 0.80")

            confidence = item.get("confidence", {})
            confidence_is_passing = (
                isinstance(confidence, dict) and confidence.get("level") in PASSING_CONFIDENCE
            )
            if not confidence_is_passing:
                messages.append(f"{path}: evidence confidence must be HIGH or MEDIUM")

            for article_index, article in enumerate(item.get("similar_articles", [])):
                if not isinstance(article, dict):
                    continue
                article_path = f"{path}/similar_articles/{article_index}"
                if not is_doi_syntax_valid(str(article.get("doi", ""))):
                    messages.append(f"{article_path}: DOI syntax is invalid")
                if article.get("integrity_status") not in PASSING_INTEGRITY:
                    messages.append(f"{article_path}: DOI integrity status is not eligible")
    return messages

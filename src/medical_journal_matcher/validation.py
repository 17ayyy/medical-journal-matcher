from __future__ import annotations

import json
from datetime import date
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
FIXED_DISCLAIMER = (
    "本结果基于用户提供的稿件信息、可访问数据源和查询当日可核验的期刊资料，仅用于辅助选刊和人工决策。"
    "匹配分及“冲刺、优先、相对稳妥”属于相对投稿策略，不是录用概率，也不构成录用保证。"
    "JIF、JCR 分区、APC、开放获取政策、投稿范围和出版速度可能变化，"
    "投稿前应在期刊官网及用户有权访问的 "
    "JCR 数据中再次核验。"
)


def validate_output(instance: dict[str, Any], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
    messages = [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in errors
    ]
    messages.extend(_validate_run_level_rules(instance))
    messages.extend(_validate_formal_recommendations(instance))
    messages.extend(_validate_candidate_buckets(instance))
    messages.extend(_validate_source_references(instance))
    return messages


def _validate_run_level_rules(instance: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    recommendations = instance.get("recommendations")
    run = instance.get("run")
    if (
        isinstance(run, dict)
        and run.get("jcr_data_mode") == "PUBLIC"
        and isinstance(recommendations, dict)
        and any(
            isinstance(recommendations.get(bucket), list) and recommendations[bucket]
            for bucket in FORMAL_TIERS
        )
    ):
        messages.append("recommendations: PUBLIC JCR mode cannot contain formal recommendations")

    disclaimers = instance.get("disclaimers")
    if isinstance(disclaimers, list) and FIXED_DISCLAIMER not in disclaimers:
        messages.append("disclaimers: the complete fixed disclaimer is required")
    return messages


def _validate_formal_recommendations(instance: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    recommendations = instance.get("recommendations")
    if not isinstance(recommendations, dict):
        return messages

    evidence_start, evidence_end = _evidence_window(instance)

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

            seen_dois: set[str] = set()
            for article_index, article in enumerate(item.get("similar_articles", [])):
                if not isinstance(article, dict):
                    continue
                article_path = f"{path}/similar_articles/{article_index}"
                doi = str(article.get("doi", ""))
                if not is_doi_syntax_valid(doi):
                    messages.append(f"{article_path}: DOI syntax is invalid")
                elif doi.lower() in seen_dois:
                    messages.append(f"{article_path}: DOI is duplicated in the recommendation")
                else:
                    seen_dois.add(doi.lower())
                if article.get("integrity_status") not in PASSING_INTEGRITY:
                    messages.append(f"{article_path}: DOI integrity status is not eligible")
                publication_date = _parse_date(article.get("publication_date"))
                if (
                    publication_date is not None
                    and evidence_start is not None
                    and evidence_end is not None
                    and not evidence_start <= publication_date <= evidence_end
                ):
                    messages.append(
                        f"{article_path}: publication_date is outside the evidence window"
                    )
    return messages


def _validate_candidate_buckets(instance: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    unverified = instance.get("unverified_candidates")
    if isinstance(unverified, list):
        for index, item in enumerate(unverified):
            if not isinstance(item, dict):
                continue
            statuses = _gate_statuses(item)
            path = f"unverified_candidates/{index}"
            if "FAIL" in statuses:
                messages.append(f"{path}: candidate with a failed gate belongs in exclusions")
            elif "UNVERIFIED" not in statuses:
                messages.append(f"{path}: candidate must have at least one unverified gate")

    excluded = instance.get("excluded_candidates")
    if isinstance(excluded, list):
        for index, item in enumerate(excluded):
            if not isinstance(item, dict):
                continue
            failed_gate = item.get("failed_gate")
            if not isinstance(failed_gate, str):
                continue
            failed_keys = {
                gate.get("gate_key")
                for gate in item.get("gates", [])
                if isinstance(gate, dict) and gate.get("status") == "FAIL"
            }
            if failed_gate not in failed_keys:
                messages.append(
                    f"excluded_candidates/{index}: failed_gate must reference a FAIL gate"
                )
    return messages


def _validate_source_references(instance: dict[str, Any]) -> list[str]:
    sources = instance.get("sources")
    if not isinstance(sources, list):
        return []
    known_ids = {
        source.get("source_fact_id")
        for source in sources
        if isinstance(source, dict) and isinstance(source.get("source_fact_id"), str)
    }
    messages: list[str] = []
    for path, candidate in _iter_candidates(instance):
        journal = candidate.get("journal")
        if isinstance(journal, dict):
            messages.extend(
                _missing_reference_messages(
                    journal.get("source_fact_ids"), known_ids, f"{path}/journal/source_fact_ids"
                )
            )
        for index, gate in enumerate(candidate.get("gates", [])):
            if isinstance(gate, dict):
                messages.extend(
                    _missing_reference_messages(
                        gate.get("evidence_ref_ids"),
                        known_ids,
                        f"{path}/gates/{index}/evidence_ref_ids",
                    )
                )
        score = candidate.get("score")
        if isinstance(score, dict):
            for index, dimension in enumerate(score.get("dimensions", [])):
                if isinstance(dimension, dict):
                    messages.extend(
                        _missing_reference_messages(
                            dimension.get("evidence_ref_ids"),
                            known_ids,
                            f"{path}/score/dimensions/{index}/evidence_ref_ids",
                        )
                    )
    return messages


def _iter_candidates(instance: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    candidates: list[tuple[str, dict[str, Any]]] = []
    recommendations = instance.get("recommendations")
    if isinstance(recommendations, dict):
        for bucket in FORMAL_TIERS:
            items = recommendations.get(bucket)
            if isinstance(items, list):
                candidates.extend(
                    (f"recommendations/{bucket}/{index}", item)
                    for index, item in enumerate(items)
                    if isinstance(item, dict)
                )
    for bucket in ("unverified_candidates", "excluded_candidates"):
        items = instance.get(bucket)
        if isinstance(items, list):
            candidates.extend(
                (f"{bucket}/{index}", item)
                for index, item in enumerate(items)
                if isinstance(item, dict)
            )
    return candidates


def _missing_reference_messages(
    references: Any, known_ids: set[Any], path: str
) -> list[str]:
    if not isinstance(references, list):
        return []
    return [
        f"{path}: unknown source_fact_id {reference!r}"
        for reference in references
        if reference not in known_ids
    ]


def _gate_statuses(candidate: dict[str, Any]) -> set[Any]:
    gates = candidate.get("gates")
    if not isinstance(gates, list):
        return set()
    return {gate.get("status") for gate in gates if isinstance(gate, dict)}


def _evidence_window(instance: dict[str, Any]) -> tuple[date | None, date | None]:
    run = instance.get("run")
    if not isinstance(run, dict):
        return None, None
    window = run.get("evidence_window")
    if not isinstance(window, dict):
        return None, None
    return _parse_date(window.get("start")), _parse_date(window.get("end"))


def _parse_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None

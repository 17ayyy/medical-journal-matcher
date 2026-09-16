from __future__ import annotations

from copy import deepcopy
from typing import Any

from medical_journal_matcher.validation import FIXED_DISCLAIMER


def valid_output(*, jcr_data_mode: str = "PUBLIC") -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "run": {
            "run_id": "test-run",
            "generated_at": "2026-09-16T00:00:00+08:00",
            "jcr_data_mode": jcr_data_mode,
            "privacy_mode": "LOCAL_PARSE_ONLY",
            "consent_record": None,
            "scoring_version": "0.1.0",
            "evidence_window": {"start": "2023-09-16", "end": "2026-09-16"},
            "source_health": {},
            "errors": [],
        },
        "manuscript_profile": {
            "input_sufficiency": "ABSTRACT",
            "primary_domain": "biomedicine",
            "specialties": ["critical care"],
            "submission_format": "ORIGINAL_ARTICLE",
            "study_designs": ["DIAGNOSTIC_ACCURACY"],
            "reporting_guidelines": ["STARD"],
            "methods": ["ultrasound"],
            "population_or_object": ["adult patients"],
            "profile_confidence": "HIGH",
        },
        "constraints": {
            "required_wos_indexes": ["SCIE"],
            "target_jcr_quartiles": ["Q1", "Q2"],
            "target_jcr_categories": ["CRITICAL CARE MEDICINE"],
            "jcr_category_match_policy": "ANY",
            "oa_requirement": "NO_REQUIREMENT",
            "apc_budget_mode": "OFF",
            "publication_speed": {},
            "publisher_preferences": [],
            "tier_counts": {},
            "privacy_mode": "LOCAL_PARSE_ONLY",
        },
        "recommendations": {"sprint": [], "priority": [], "relatively_safe": []},
        "unverified_candidates": [],
        "excluded_candidates": [],
        "submission_readiness": None,
        "sources": [],
        "disclaimers": [FIXED_DISCLAIMER],
    }


def candidate(*, gate_status: str = "PASS") -> dict[str, Any]:
    return {
        "journal": {
            "journal_id": "journal-1",
            "journal_title_original": "Example Medical Journal",
            "publisher_original": "Example Publisher",
            "issn_l": "2049-3630",
            "pissn": "2049-3630",
            "eissn": None,
            "official_urls": {},
            "source_fact_ids": [],
        },
        "gates": [
            {
                "gate_key": "jcr",
                "status": gate_status,
                "reason_zh": "测试门槛",
                "evidence_ref_ids": [],
            }
        ],
        "score": {
            "final_match_score": 90.0,
            "score_coverage": 1.0,
            "scoring_version": "0.1.0",
            "dimensions": [],
        },
        "confidence": {
            "level": "HIGH" if gate_status == "PASS" else "LOW",
            "reasons_zh": [],
            "input_sufficiency": 1.0,
            "evidence_sufficiency": 1.0,
            "provenance_completeness": 1.0,
            "signal_agreement": 1.0,
            "stability": 1.0,
            "freshness": 1.0,
        },
    }


def recommendation(*, tier: str = "PRIORITY") -> dict[str, Any]:
    item = deepcopy(candidate())
    item.update(
        {
            "strategy_tier": tier,
            "tier_rationale_zh": "满足正式推荐条件",
            "similar_articles": [
                {
                    "title_original": "A relevant study",
                    "publication_date": "2025-01-01",
                    "date_type": "published_online",
                    "journal_title_original": "Example Medical Journal",
                    "article_type_original": "Original Article",
                    "doi": "10.1000/example.1",
                    "source_ids": ["crossref:example.1"],
                    "integrity_status": "CLEAR",
                    "match_reasons_zh": ["研究设计相近"],
                }
            ],
            "strengths_zh": [],
            "mismatches_zh": [],
            "manual_checks_zh": [],
        }
    )
    return item

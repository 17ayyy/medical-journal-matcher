from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

OUTBOUND_QUERY_FIELDS = frozenset(
    {
        "topics",
        "diseases_or_processes",
        "population_or_object",
        "submission_format",
        "study_designs",
        "methods",
        "outcome_categories",
        "contribution_type",
        "mesh_terms",
        "synonyms",
    }
)


def build_outbound_query(profile: Mapping[str, Any]) -> dict[str, Any]:
    """Build a fail-closed query payload from structured, non-manuscript fields."""
    disallowed = set(profile) - OUTBOUND_QUERY_FIELDS
    if disallowed:
        names = ", ".join(sorted(disallowed))
        raise ValueError(f"Profile contains non-allowlisted outbound fields: {names}")

    payload: dict[str, Any] = {}
    for key, value in profile.items():
        if value is None or value == "" or value == []:
            continue
        if isinstance(value, str):
            payload[key] = value.strip()
        elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
            payload[key] = [str(item).strip() for item in value if str(item).strip()]
        else:
            raise TypeError(f"Outbound field {key!r} must be a string or sequence")
    return payload

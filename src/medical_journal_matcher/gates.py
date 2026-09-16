from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum


class GateStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNVERIFIED = "UNVERIFIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class CandidateDisposition(StrEnum):
    ELIGIBLE = "ELIGIBLE"
    UNVERIFIED = "UNVERIFIED"
    EXCLUDED = "EXCLUDED"


@dataclass(frozen=True)
class GateResult:
    gate_key: str
    status: GateStatus
    enabled: bool = True
    reason_zh: str = ""


def classify_gates(gates: Iterable[GateResult]) -> CandidateDisposition:
    """Apply the PRD fail-closed hard-gate state machine."""
    enabled = [gate for gate in gates if gate.enabled]
    if not enabled:
        return CandidateDisposition.UNVERIFIED
    if any(gate.status is GateStatus.FAIL for gate in enabled):
        return CandidateDisposition.EXCLUDED
    if any(gate.status is GateStatus.UNVERIFIED for gate in enabled):
        return CandidateDisposition.UNVERIFIED
    if all(gate.status in {GateStatus.PASS, GateStatus.NOT_APPLICABLE} for gate in enabled):
        return CandidateDisposition.ELIGIBLE
    return CandidateDisposition.UNVERIFIED

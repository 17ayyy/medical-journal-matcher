from medical_journal_matcher.gates import (
    CandidateDisposition,
    GateResult,
    GateStatus,
    classify_gates,
)


def test_unverified_gate_never_becomes_eligible() -> None:
    gates = [
        GateResult("wos", GateStatus.PASS),
        GateResult("jcr", GateStatus.UNVERIFIED),
    ]
    assert classify_gates(gates) is CandidateDisposition.UNVERIFIED


def test_fail_takes_precedence() -> None:
    gates = [
        GateResult("wos", GateStatus.FAIL),
        GateResult("jcr", GateStatus.UNVERIFIED),
    ]
    assert classify_gates(gates) is CandidateDisposition.EXCLUDED


def test_no_enabled_gates_fails_closed() -> None:
    assert classify_gates([]) is CandidateDisposition.UNVERIFIED
    assert (
        classify_gates([GateResult("optional", GateStatus.PASS, enabled=False)])
        is CandidateDisposition.UNVERIFIED
    )

import copy
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from qref import checks, contracts, execution, report

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "cases" / "qaoa.json"
ENVS = ROOT / ".qref" / "envs"
HAVE_ENVS = (ENVS / "reference" / "bin" / "python").exists() and (ENVS / "target" / "bin" / "python").exists()


def small_case():
    case = json.loads(CASE.read_text())
    case["graphs"] = [{"id": "pair", "nodes": [0, 1], "edges": [[0, 1]]}]
    case["angles"] = [{"id": "a", "theta": [0.3, 0.7]}]
    case["shots"] = [8]
    return case


def completed(e, completed_shots=8, counts=None):
    counts = counts or {"01": 4, "10": 4}
    probs = [0.0, 0.5, 0.5, 0.0]
    return {"id": e["id"], "input_sha256": e["input_sha256"], "state": "completed", "reason_code": None,
            "circuit": {"measurement_map": [[0, 0], [1, 1]], "qasm": "x.qasm"},
            "sampling": {"requested_shots": e["requested_shots"], "completed_shots": completed_shots,
                         "count_sum": sum(counts.values()), "counts": counts},
            "numeric": {"returned": -1.0, "module_on_counts": -1.0, "probabilities": probs,
                        "module_on_probabilities": -1.0}}


def doc(recs):
    rows = [{"k": k, "maxcut_obj": float(checks.negative_cut(k, [[0, 1]])),
             "compute_expectation": float(checks.negative_cut(k, [[0, 1]]))} for k in range(4)]
    return {"executions": recs, "classical_tables": [{"graph_id": "pair", "n": 2, "rows": rows}]}


PASS_CIRCUIT = {"id": "circuit-result-x", "criterion": "equivalent", "status": "pass", "reason_code": "equal"}


def build(ref_recs, tgt_recs, failures=None, circuit=PASS_CIRCUIT):
    expected = contracts.expected_executions(small_case())
    circuits = {e["id"]: circuit for e in expected} if circuit else {}
    return expected, checks.build(expected, {"reference": doc(ref_recs(expected)), "target": doc(tgt_recs(expected))},
                                  circuits, failures or {"reference": None, "target": None})


def test_identical_complete_evidence_is_consistent():
    _, (rows, findings, state, summary, counts, _) = build(lambda ex: [completed(ex[0])], lambda ex: [completed(ex[0])])
    assert (state, summary, findings) == ("complete", "consistent", [])
    assert counts["pass"] == len(rows)


def test_shot_difference_is_one_reviewable_finding():
    _, (_, findings, state, summary, _, _) = build(lambda ex: [completed(ex[0], 16, {"01": 8, "10": 8})],
                                                   lambda ex: [completed(ex[0])])
    assert (state, summary) == ("complete", "difference")
    assert [f["id"] for f in findings] == ["shot_policy"]


def test_sampling_integrity_error_invalidates_and_is_never_a_finding():
    _, (rows, findings, state, summary, _, _) = build(lambda ex: [completed(ex[0], 8, {"01": 4, "10": 3})],
                                                      lambda ex: [completed(ex[0])])
    assert state == "invalid" and summary == "incomplete"
    assert not any(f["id"] == "shot_policy" for f in findings)
    integrity = next(c for c in rows if c["id"].startswith("shots-integrity/reference"))
    assert (integrity["status"], integrity["reason_code"]) == ("error", "invalid_sampling")


def test_interrupted_worker_is_not_a_completed_pair():
    def interrupted(ex):
        rec = completed(ex[0])
        rec.update(state="incomplete", reason_code=None, sampling=None, numeric=None)
        return [rec]
    _, (rows, _, state, summary, _, coverage) = build(interrupted, lambda ex: [completed(ex[0])],
                                                      failures={"reference": "worker_timeout", "target": None})
    assert coverage["completed_pairs"] == 0
    assert state == "failed" and summary == "incomplete"  # a timed-out worker with zero completed pairs
    assert next(c for c in rows if c["kind"] == "circuit")["reason_code"] == "worker_interrupted"


def test_failed_execution_with_no_pairs_is_failed():
    def failed(ex):
        rec = completed(ex[0])
        rec.update(state="failed", reason_code="worker_failed", sampling=None, numeric=None)
        return [rec]
    _, (_, _, state, _, _, _) = build(failed, lambda ex: [completed(ex[0])])
    assert state == "failed"


def test_input_digest_mismatch_is_invalid_pairing():
    def tampered(ex):
        rec = completed(ex[0])
        rec["input_sha256"] = "0" * 64
        return [rec]
    _, (rows, _, state, _, _, _) = build(tampered, lambda ex: [completed(ex[0])])
    assert state == "invalid"
    assert next(c for c in rows if c["id"] == "pairing")["status"] == "error"


@pytest.mark.parametrize("criterion,status", [("equivalent_up_to_global_phase", "pass"),
                                              ("equivalent_up_to_phase", "inconclusive"),
                                              ("probably_equivalent", "inconclusive"),
                                              ("not_equivalent", "difference")])
def test_checker_criteria_never_overclaim(criterion, status):
    assert checks.QCEC_MAP[criterion][0] == status


@pytest.mark.parametrize("mutate,message", [
    (lambda c: c.update(shots=[True]), "boolean"),
    (lambda c: c["angles"].append(dict(c["angles"][0])), "duplicate angles"),
    (lambda c: c["graphs"][0].update(edges=[[0, 1], [1, 0]]), "duplicate edge"),
    (lambda c: c["angles"][0].update(theta=[0.1]), "even length"),
    (lambda c: c.update(schema="qref.qaoa-case/v2"), "schema"),
])
def test_invalid_cases_are_rejected(mutate, message):
    case = small_case()
    mutate(case)
    with pytest.raises(contracts.ContractError):
        contracts.validate_case(case)


def test_duplicate_json_keys_and_nan_rejected():
    with pytest.raises(contracts.ContractError):
        contracts.load_json_bytes(b'{"a": 1, "a": 2}')
    with pytest.raises(contracts.ContractError):
        contracts.load_json_bytes(b'{"a": NaN}')


def run_case(tmp_path, case, name):
    case_path = CASE.parent / f".test-{name}.json"
    case_path.write_text(json.dumps(case))
    try:
        out = tmp_path / name
        code = execution.run(case_path, ENVS / "reference/bin/python", ENVS / "target/bin/python", out, True)
    finally:
        case_path.unlink()
    return code, out, json.loads((out / "evidence.json").read_text())


@pytest.mark.skipif(not HAVE_ENVS, reason="pinned reference/target environments not provisioned")
def test_seeded_decoder_regression_is_caught_with_equivalent_circuits(tmp_path):
    """Seeded regression (labelled): the target decodes Qiskit count strings without reversing them."""
    port = (ROOT / "evidence/qaoa/port_functions.py").read_text()
    assert "bitstring[::-1]" in port
    seeded = tmp_path / "seeded_target.py"
    seeded.write_text(port.replace("bitstring[::-1]", "bitstring"))
    case = json.loads(CASE.read_text())
    case["origin"] = "seeded_regression"
    case["graphs"] = [g for g in case["graphs"] if g["id"] == "asymmetric4"]
    case["shots"] = [512]
    case["target"]["module"] = str(Path(os.path.relpath(seeded, CASE.parent)))
    code, out, evidence = run_case(tmp_path, case, "seeded")
    kinds = {f["id"] for f in evidence["findings"]}
    assert code == 1
    assert "classical-basis" in kinds and "exact-objective" not in kinds
    assert all(c["status"] == "pass" for c in evidence["checks"] if c["kind"] == "circuit")
    report.verify_bundle(out)


@pytest.mark.skipif(not HAVE_ENVS, reason="pinned reference/target environments not provisioned")
def test_tampering_and_hostile_strings(tmp_path):
    case = json.loads(CASE.read_text())
    case["title"] = '</title><script>alert(1)</script>'
    case["graphs"], case["angles"], case["shots"] = case["graphs"][:1], case["angles"][:1], [17]
    _, out, _ = run_case(tmp_path, case, "hostile")
    html = (out / "index.html").read_text()
    assert "<script>alert(1)" not in html and "&lt;script&gt;alert(1)" in html
    moved = tmp_path / "moved"
    shutil.copytree(out, moved)
    report.verify_bundle(moved)
    (moved / "artifacts/target/observations.json").write_text("{}")
    with pytest.raises(contracts.ContractError, match="changed"):
        report.verify_bundle(moved)
    shutil.copytree(out, tmp_path / "extra")
    (tmp_path / "extra" / "note.txt").write_text("x")
    with pytest.raises(contracts.ContractError, match="undeclared"):
        report.verify_bundle(tmp_path / "extra")


@pytest.mark.skipif(not HAVE_ENVS, reason="pinned reference/target environments not provisioned")
def test_trust_flag_required_and_stale_proposal_rejected(tmp_path):
    with pytest.raises(contracts.ContractError, match="trust-local-code"):
        execution.run(CASE, ENVS / "reference/bin/python", ENVS / "target/bin/python", tmp_path / "x", False)
    record = tmp_path / "proposal.json"
    record.write_text(json.dumps({"output_sha256": "0" * 64, "reference_sha256": "0" * 64}))
    case = json.loads(CASE.read_text())
    case["proposal"] = {"record": os.path.relpath(record, CASE.parent)}
    with pytest.raises(contracts.ContractError, match="stale"):
        run_case(tmp_path, case, "stale")


EXAMPLE = ROOT / "examples" / "qaoa-run"


def filled_template(**changes):
    template = json.loads((EXAMPLE / "review-template.json").read_text())
    entry = template["decisions"][0]
    entry.update(decision="accepted_intentional", reviewer="Test Reviewer (synthetic)",
                 reason="Synthetic test decision.", recorded_at="2026-10-25T22:00:00Z")
    entry.update(changes)
    return template


def test_decision_overlay_changes_only_the_review_state(tmp_path):
    decisions = tmp_path / "review.json"
    decisions.write_text(json.dumps(filled_template()))
    out = tmp_path / "reviewed"
    report.rerender(EXAMPLE, out, decisions)
    assert (out / "evidence.json").read_bytes() == (EXAMPLE / "evidence.json").read_bytes()
    html = (out / "index.html").read_text()
    assert "Accepted as intentional" in html and "Human review: recorded acceptance" in html
    report.verify_bundle(out)
    (out / "decisions.json").write_text(json.dumps(filled_template(decision="rejected")))
    with pytest.raises(contracts.ContractError, match="decisions.json"):
        report.verify_bundle(out)


@pytest.mark.parametrize("changes,message", [
    ({"reviewer": None}, "filled in"),
    ({"finding_id": "circuit"}, "unknown finding"),
    ({"recorded_at": "yesterday"}, "UTC"),
])
def test_invalid_decisions_are_refused(tmp_path, changes, message):
    decisions = tmp_path / "review.json"
    decisions.write_text(json.dumps(filled_template(**changes)))
    with pytest.raises(contracts.ContractError, match=message):
        report.rerender(EXAMPLE, tmp_path / "out", decisions)
    assert not (tmp_path / "out").exists()


def test_decision_for_other_evidence_is_refused(tmp_path):
    template = filled_template()
    template["evidence_sha256"] = "0" * 64
    decisions = tmp_path / "review.json"
    decisions.write_text(json.dumps(template))
    with pytest.raises(contracts.ContractError, match="different evidence"):
        report.rerender(EXAMPLE, tmp_path / "out", decisions)


def test_replaced_zip_fails_even_when_loose_files_are_intact(tmp_path):
    import zipfile
    out = tmp_path / "copy"
    report.rerender(EXAMPLE, out)
    report.verify_bundle(out)
    names = zipfile.ZipFile(out / "evidence.zip").namelist()
    assert "evidence.json" in names and "manifest.json" in names and "evidence.zip" not in names
    with zipfile.ZipFile(out / "evidence.zip", "w") as z:
        for name in names:
            z.writestr(name, b"{}" if name == "evidence.json" else (out / name).read_bytes())
    with pytest.raises(contracts.ContractError, match="evidence.zip member differs"):
        report.verify_bundle(out)


def seeded_target(tmp_path, old, new, name):
    port = (ROOT / "evidence/qaoa/port_functions.py").read_text()
    assert old in port
    path = tmp_path / f"{name}.py"
    path.write_text(port.replace(old, new, 1))
    case = json.loads(CASE.read_text())
    case["origin"] = "seeded_regression"
    case["graphs"], case["angles"], case["shots"] = case["graphs"][:1], case["angles"][:1], [17]
    case["target"]["module"] = os.path.relpath(path, CASE.parent)
    return case


@pytest.mark.skipif(not HAVE_ENVS, reason="pinned reference/target environments not provisioned")
def test_gate_after_measurement_is_unsupported_not_a_pass(tmp_path):
    case = seeded_target(tmp_path, "    qc.measure_all()", "    qc.measure_all()\n    qc.x(0)", "after_measure")
    code, out, evidence = run_case(tmp_path, case, "unsupported")
    assert code == 2 and evidence["evidence_summary"] == "incomplete"
    assert evidence["run_state"] == "partial"
    reasons = {c["reason_code"] for c in evidence["checks"] if c["status"] == "unsupported"}
    assert "unsupported_measurement" in reasons
    assert "Comparison incomplete" in (out / "index.html").read_text()
    report.verify_bundle(out)


@pytest.mark.skipif(not HAVE_ENVS, reason="pinned reference/target environments not provisioned")
def test_import_failure_is_a_failed_run_with_diagnostics(tmp_path):
    case = seeded_target(tmp_path, "import networkx as nx", "import networkx as nx\nraise RuntimeError('seeded import failure')", "bad_import")
    code, out, evidence = run_case(tmp_path, case, "import")
    assert code == 2 and evidence["run_state"] == "failed"
    assert evidence["provenance"]["side_failures"]["target"] == "import_failed"
    assert "seeded import failure" in (out / "artifacts/target/error-import.txt").read_text()
    assert "Execution failed" in (out / "index.html").read_text()


@pytest.mark.skipif(not HAVE_ENVS, reason="pinned reference/target environments not provisioned")
def test_worker_deadline_kills_and_reports_without_fabricating(tmp_path, monkeypatch):
    monkeypatch.setattr(execution, "OBSERVATION_DEADLINE", 8)
    case = seeded_target(tmp_path, "import networkx as nx", "import networkx as nx\nimport time\ntime.sleep(60)", "slow")
    code, out, evidence = run_case(tmp_path, case, "slow")
    assert code == 2 and evidence["run_state"] == "failed"
    assert evidence["provenance"]["side_failures"]["target"] == "worker_timeout"
    assert evidence["coverage"]["completed_pairs"] == 0


@pytest.mark.skipif(not HAVE_ENVS, reason="pinned reference/target environments not provisioned")
def test_missing_interpreter_is_reported_not_substituted(tmp_path):
    case_path = CASE.parent / ".test-missing.json"
    case = json.loads(CASE.read_text())
    case["graphs"], case["angles"], case["shots"] = case["graphs"][:1], case["angles"][:1], [17]
    case_path.write_text(json.dumps(case))
    try:
        code = execution.run(case_path, tmp_path / "no-such/bin/python", ENVS / "target/bin/python", tmp_path / "m", True)
    finally:
        case_path.unlink()
    evidence = json.loads((tmp_path / "m/evidence.json").read_text())
    assert code == 2 and evidence["run_state"] == "failed"
    assert evidence["provenance"]["side_failures"]["reference"] == "environment_mismatch"
    assert evidence["provenance"]["reference_environment"] is None


@pytest.mark.skipif(not HAVE_ENVS, reason="pinned reference/target environments not provisioned")
@pytest.mark.parametrize("setting,value,reason", [("QCEC_DEADLINE", 0.001, "timeout"),
                                                  ("QCEC_BUDGET", 0, "checker_budget_exhausted")])
def test_checker_timeout_never_becomes_equivalent(tmp_path, monkeypatch, setting, value, reason):
    monkeypatch.setattr(execution, setting, value)
    case = json.loads(CASE.read_text())
    case["graphs"], case["angles"], case["shots"] = case["graphs"][:1], case["angles"][:1], [17]
    code, out, evidence = run_case(tmp_path, case, reason)
    circuit = [c for c in evidence["checks"] if c["kind"] == "circuit"]
    assert circuit and all((c["status"], c["reason_code"]) == ("inconclusive", reason) for c in circuit)
    assert code == 2 and evidence["evidence_summary"] == "incomplete"
    assert "Circuit result: inconclusive" in (out / "index.html").read_text() or "Comparison incomplete" in (out / "index.html").read_text()


@pytest.mark.skipif(not HAVE_ENVS, reason="pinned reference/target environments not provisioned")
def test_seeded_rotation_change_is_a_circuit_difference(tmp_path):
    case = seeded_target(tmp_path, "qc.rx(2 * beta[irep], i)", "qc.rx(beta[irep], i)", "rotation")
    code, out, evidence = run_case(tmp_path, case, "rotation")
    assert code == 1 and evidence["findings"][0]["id"] == "circuit"
    circuit = [c for c in evidence["checks"] if c["kind"] == "circuit"]
    assert all((c["status"], c["observed"]) == ("difference", "not_equivalent") for c in circuit)
    assert "Circuit differences." in (out / "index.html").read_text()


@pytest.mark.skipif(not HAVE_ENVS, reason="pinned reference/target environments not provisioned")
def test_second_backend_run_is_unsupported(tmp_path):
    case = seeded_target(tmp_path, "        counts = backend.run(",
                         "        backend.run(tqc, shots=1).result()\n        counts = backend.run(", "two_runs")
    code, _, evidence = run_case(tmp_path, case, "two_runs")
    assert code == 2
    assert {c["reason_code"] for c in evidence["checks"] if c["status"] == "unsupported"} == {"unsupported_backend_execution"}


@pytest.mark.parametrize("decision,finding_label,summary", [
    ("rejected", "Change rejected", "Human review: changes rejected"),
    ("needs_review", "Needs review", "Human review: pending"),
    ("accepted_intentional", "Accepted as intentional", "Human review: recorded acceptance"),
])
def test_every_review_label(tmp_path, decision, finding_label, summary):
    decisions = tmp_path / "review.json"
    decisions.write_text(json.dumps(filled_template(decision=decision)))
    report.rerender(EXAMPLE, tmp_path / "out", decisions)
    html = (tmp_path / "out" / "index.html").read_text()
    assert f"<strong>{finding_label}</strong>" in html and summary in html


def test_clean_control_needs_no_review():
    html = (ROOT / "examples/positive-control/index.html").read_text()
    assert "Human review: not required" in html and "No differences" in html

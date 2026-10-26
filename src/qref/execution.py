"""`qref run`: snapshot inputs, execute both pinned runtimes, check, and write the evidence bundle."""
from __future__ import annotations

import json
import mimetypes
import os
import shutil
import signal
import subprocess
from importlib import resources
from pathlib import Path

from . import __version__, checks, contracts, report

OBSERVATION_DEADLINE = 120
QCEC_DEADLINE = 30
QCEC_BUDGET = 120
LOG_LIMIT = 1024 * 1024
SIDES = ("reference", "target")

ENV_PROBE = (
    "import json,platform;from importlib import metadata;"
    "print(json.dumps({'python_version':platform.python_version(),'os':platform.system(),"
    "'architecture':platform.machine(),'distributions':sorted({(d.metadata['Name'] or '').lower().replace('_','-'):"
    "d.version for d in metadata.distributions()}.items())}))"
)

LIMITATIONS = [
    "Checks cover only the declared graphs, angles and shot requests.",
    "Numerical agreement uses floating-point arithmetic with absolute tolerance 1e-10.",
    "No optimizer convergence, hardware, noise, dynamic-circuit or whole-program claim.",
    "The reference is a preservation baseline, not scientific truth.",
    "Candidate code ran locally as trusted, inspected code; virtual environments isolate versions, not hostile code.",
    "Hashes show internal consistency; they are not a signature or an independent attestation.",
]


def _run_bounded(argv, cwd: Path, timeout: int, stdout_path: Path, stderr_path: Path):
    """Run argv in its own process group; kill the group on deadline. Returns (exit_code or None, timed_out)."""
    with open(stdout_path, "wb") as out, open(stderr_path, "wb") as err:
        proc = subprocess.Popen(argv, cwd=cwd, stdout=out, stderr=err, start_new_session=True)
        try:
            return proc.wait(timeout=timeout), False
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            return None, True
        finally:
            for p in (stdout_path, stderr_path):
                if p.stat().st_size > LOG_LIMIT:
                    data = p.read_bytes()[:LOG_LIMIT]
                    p.write_bytes(data + b"\n[truncated by qref at 1 MiB]\n")


def _probe_environment(python: Path, pins: dict, cwd: Path):
    try:
        out = subprocess.run([str(python), "-I", "-c", ENV_PROBE], cwd=cwd, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, [f"interpreter unavailable: {exc}"]
    if out.returncode != 0:
        return None, [f"interpreter probe failed: {out.stderr.strip()[-500:]}"]
    env = json.loads(out.stdout)
    installed = dict(env["distributions"])
    env["distributions"] = [{"name": n, "version": v} for n, v in env["distributions"] if n]
    problems = [f"{name}: pinned {version}, installed {installed.get(name, 'missing')}"
                for name, version in sorted(pins.items()) if installed.get(name) != version]
    return env, problems


def _copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def _inventory(out: Path):
    rows = []
    for path in sorted((out / "artifacts").rglob("*")):
        if path.is_file():
            rel = path.relative_to(out).as_posix()
            media = mimetypes.guess_type(path.name)[0] or {
                ".qasm": "text/plain", ".qpy": "application/octet-stream", ".py": "text/x-python"}.get(path.suffix, "text/plain")
            rows.append({"path": rel, "size": path.stat().st_size, "media_type": media,
                         "sha256": contracts.sha256_file(path)})
    return rows


def run(case_path: Path, reference_python: Path, target_python: Path, out: Path, trust_local_code: bool) -> int:
    if not trust_local_code:
        raise contracts.ContractError("--trust-local-code is required: candidate Python can read files, use the "
                                      "network and access process credentials. Only run inspected code.")
    case, case_bytes = contracts.load_case(case_path)
    base = case_path.parent
    out.mkdir(parents=True, exist_ok=False)
    started = contracts.utc_now()
    inputs = out / "artifacts" / "inputs"

    # 1. Snapshot every input; workers read only these copies.
    _copy(case_path, inputs / "case.original.json")
    portable = json.loads(json.dumps(case))
    receipts = {}
    proposal_record = None
    for side in SIDES:
        decl = case[side]
        module_src = base / decl["module"]
        _copy(module_src, inputs / f"{side}.py")
        _copy(base / decl["pins"], inputs / f"{side}-pins.txt")
        _copy(base / decl["receipt"]["license_file"], inputs / f"{side}-LICENSE.txt")
        portable[side] = {"module": f"artifacts/inputs/{side}.py", "pins": f"artifacts/inputs/{side}-pins.txt",
                          "receipt": {**decl["receipt"], "license_file": f"artifacts/inputs/{side}-LICENSE.txt"}}
        receipts[side] = {**decl["receipt"],
                          "module_sha256": contracts.sha256_file(inputs / f"{side}.py"),
                          "license_artifact": f"artifacts/inputs/{side}-LICENSE.txt",
                          "license_sha256": contracts.sha256_file(inputs / f"{side}-LICENSE.txt")}
    if case["proposal"] is not None:
        record_src = base / case["proposal"]["record"]
        proposal_record = contracts.load_json_bytes(record_src.read_bytes())
        if proposal_record.get("output_sha256") != receipts["target"]["module_sha256"]:
            raise contracts.ContractError("proposal attribution is stale: the target bytes differ from the recorded model output")
        if proposal_record.get("reference_sha256") != receipts["reference"]["module_sha256"]:
            raise contracts.ContractError("proposal attribution is stale: the reference differs from the proposal input")
        _copy(record_src, inputs / "proposal.json")
        portable["proposal"] = {"record": "artifacts/inputs/proposal.json"}
    if receipts["target"]["derived_from_sha256"] not in (None, receipts["reference"]["module_sha256"]):
        raise contracts.ContractError("target receipt derives from a different reference module")
    portable_bytes = contracts.record_bytes(portable)
    (out / "case.json").write_bytes(portable_bytes)

    expected = contracts.expected_executions(case)
    pythons = {"reference": reference_python.absolute(), "target": target_python.absolute()}
    target_python = pythons["target"]
    worker = Path(str(resources.files("qref").joinpath("_worker.py")))
    qcec_worker = Path(str(resources.files("qref").joinpath("_qcec_worker.py")))

    # 2. Execute each side in its own interpreter, serially.
    docs, environments, side_failures = {}, {}, {}
    for side in SIDES:
        side_dir = out / "artifacts" / side
        side_dir.mkdir(parents=True)
        pins = contracts.read_pins(inputs / f"{side}-pins.txt")
        env, problems = _probe_environment(pythons[side], pins, side_dir)
        environments[side] = env
        side_failures[side] = None
        if problems:
            (side_dir / "environment-mismatch.txt").write_text("\n".join(problems) + "\n", encoding="utf-8")
            side_failures[side] = "environment_mismatch"
            docs[side] = None
            continue
        runtime = {
            "side": side,
            "module_path": f"../inputs/{side}.py",
            "module_sha256": receipts[side]["module_sha256"],
            "graphs": case["graphs"],
            "executions": expected,
        }
        (side_dir / "runtime.json").write_text(json.dumps(runtime, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        code, timed_out = _run_bounded(
            [str(pythons[side]), "-I", "-B", str(worker), "runtime.json", "."],
            side_dir, OBSERVATION_DEADLINE, side_dir / "stdout.txt", side_dir / "stderr.txt")
        doc_path = side_dir / "observations.json"
        doc = json.loads(doc_path.read_text(encoding="utf-8")) if doc_path.exists() else None
        if timed_out:
            side_failures[side] = "worker_timeout"
        elif code != 0:
            side_failures[side] = "worker_failed"
        elif doc is not None and doc["import"]["state"] in ("failed", "unsupported"):
            side_failures[side] = doc["import"]["reason_code"]
        if doc is not None and side_failures[side] in ("worker_timeout", "worker_failed"):
            for rec in doc["executions"]:
                if rec["state"] in ("incomplete", "not_run") and not rec["reason_code"]:
                    rec["reason_code"] = side_failures[side] if rec["state"] == "not_run" else "worker_interrupted"
        docs[side] = doc

    # 3. Check actually submitted circuits; deduplicate identical engine inputs within this run.
    circuit_results, checker_info, unique = {}, None, {}
    for e in expected:
        recs = [next((r for r in (docs[s] or {}).get("executions", []) if r["id"] == e["id"]), None) for s in SIDES]
        if not all(r and r["state"] == "completed" for r in recs):
            continue
        paths = [out / "artifacts" / s / r["circuit"]["qasm"] for s, r in zip(SIDES, recs)]
        key = tuple(contracts.sha256_file(p) for p in paths)
        unique.setdefault(key, {"paths": paths, "executions": []})["executions"].append(e["id"])
    check_dir = out / "artifacts" / "checks"
    check_dir.mkdir(parents=True)
    spent = 0.0
    raw_results = []
    for index, (key, item) in enumerate(unique.items()):
        stem = f"pair-{index:02d}"
        if spent >= QCEC_BUDGET:
            raw_results.append((key, item, None, "checker_budget_exhausted"))
            continue
        import time
        t0 = time.monotonic()
        code, timed_out = _run_bounded(
            [str(target_python), "-I", "-B", str(qcec_worker), os.path.relpath(item["paths"][0], check_dir),
             os.path.relpath(item["paths"][1], check_dir)],
            check_dir, QCEC_DEADLINE, check_dir / f"{stem}.json", check_dir / f"{stem}.stderr.txt")
        spent += time.monotonic() - t0
        if timed_out:
            raw_results.append((key, item, None, "timeout"))
        elif code != 0:
            raw_results.append((key, item, None, "checker_exception"))
        else:
            raw = json.loads((check_dir / f"{stem}.json").read_text(encoding="utf-8"))
            checker_info = checker_info or raw
            raw_results.append((key, item, raw, None))
    checker_config = {
        "entrypoint": "mqt.qcec.verify",
        "kwargs": {},
        "importer_policy": "qiskit.qasm2.loads with LEGACY_CUSTOM_INSTRUCTIONS",
        "global_phase_policy": "global phase ignored; relative phase is a difference",
        "checker_version": (checker_info or {}).get("checker_version"),
        "qiskit_version": (checker_info or {}).get("qiskit_version"),
        "effective_defaults": None,
        "unknown_reasons": ["effective_defaults: the pinned default call does not export its configuration"],
    }
    config_sha = contracts.canonical_sha256(checker_config)
    circuit_result_rows = []
    for key, item, raw, failure in raw_results:
        cid = "circuit-result-" + contracts.canonical_sha256(
            {"reference_qasm_sha256": key[0], "target_qasm_sha256": key[1], "checker_config_sha256": config_sha})
        if raw is not None:
            criterion = raw["criterion"]
            status, reason = checks.QCEC_MAP.get(criterion, ("inconclusive", "checker_unknown"))
        else:
            criterion = None
            status, reason = ("error", "checker_exception") if failure == "checker_exception" else ("inconclusive", failure)
        row = {"id": cid, "reference_qasm_sha256": key[0], "target_qasm_sha256": key[1],
               "checker_config_sha256": config_sha, "criterion": criterion, "status": status,
               "reason_code": reason, "execution_ids": item["executions"]}
        circuit_result_rows.append(row)
        for eid in item["executions"]:
            circuit_results[eid] = row

    check_rows, findings, run_state, summary, counts, coverage = checks.build(
        expected, docs, circuit_results, side_failures)

    finished = contracts.utc_now()
    evidence = {
        "schema": "qref.evidence/v1",
        "case": {
            "definition": case,
            "case_sha256": contracts.sha256_bytes(case_bytes),
            "source_artifact": "artifacts/inputs/case.original.json",
            "portable_case_artifact": "case.json",
            "portable_case_sha256": contracts.sha256_bytes(portable_bytes),
            "executions": expected,
        },
        "provenance": {
            "tool_version": __version__,
            "observer_sha256": contracts.sha256_file(worker),
            "comparison_sha256": contracts.sha256_file(Path(checks.__file__)),
            "checker_worker_sha256": contracts.sha256_file(qcec_worker),
            "reference_sha256": receipts["reference"]["module_sha256"],
            "target_sha256": receipts["target"]["module_sha256"],
            "reference_pins_sha256": contracts.sha256_file(inputs / "reference-pins.txt"),
            "target_pins_sha256": contracts.sha256_file(inputs / "target-pins.txt"),
            "source_receipts": receipts,
            "started_at": started,
            "finished_at": finished,
            "reference_environment": environments["reference"],
            "target_environment": environments["target"],
            "side_failures": side_failures,
            "checker_config": checker_config,
            "proposal": None if proposal_record is None else {
                "artifact": "artifacts/inputs/proposal.json",
                "sha256": contracts.sha256_file(inputs / "proposal.json"),
                "resolved_model": proposal_record.get("resolved_model"),
                "cli_version": proposal_record.get("cli_version"),
                "started_at": proposal_record.get("started_at"),
                "finished_at": proposal_record.get("finished_at"),
                "summary": proposal_record["output"]["summary"],
                "intentional_changes": proposal_record["output"]["intentional_changes"],
                "uncertainties": proposal_record["output"]["uncertainties"],
                "prompt_states_known_shot_issue": proposal_record.get("prompt_states_known_shot_issue"),
            },
            "trusted_local_code": True,
            "unknown_reasons": [],
        },
        "artifacts": _inventory(out),
        "coverage": coverage,
        "circuit_results": circuit_result_rows,
        "checks": check_rows,
        "findings": findings,
        "run_state": run_state,
        "evidence_summary": summary,
        "status_counts": counts,
        "limitations": LIMITATIONS,
    }
    contracts.validate("evidence", evidence)
    evidence_bytes = contracts.record_bytes(evidence)
    (out / "evidence.json").write_bytes(evidence_bytes)
    template = {"schema": "qref.decisions/v1", "evidence_sha256": contracts.sha256_bytes(evidence_bytes),
                "decisions": [{"finding_id": f["id"], "decision": "needs_review", "reviewer": None, "reason": None,
                               "recorded_at": None} for f in findings]}
    (out / "review-template.json").write_bytes(contracts.record_bytes(template))
    report.write_export(out)
    report.verify_bundle(out)
    if run_state == "complete" and summary == "consistent":
        return 0
    if run_state == "complete" and summary == "difference":
        return 1
    return 2

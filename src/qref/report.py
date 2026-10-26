"""Render a finding-first HTML report from verified evidence and verify export bundles.

Imports no quantum library and never executes candidate code.
"""
from __future__ import annotations

import base64
import difflib
import hashlib
import json
import shutil
from importlib import resources
from pathlib import Path, PurePosixPath

import jinja2

from . import contracts

GENERATED = ("index.html", "manifest.json")


def _view(out: Path, evidence: dict, evidence_sha: str) -> dict:
    checks = evidence["checks"]
    by_id = {c["id"]: c for c in checks}
    state, summary = evidence["run_state"], evidence["evidence_summary"]
    executions = evidence["case"]["executions"]
    circuit_checks = [by_id.get(f"circuit/{e['id']}") for e in executions]
    circuit_status = {c["status"] for c in circuit_checks if c}
    if circuit_status == {"pass"}:
        circuit_line = "Equivalent circuits."
        circuit_label = "Circuits: equivalent on declared cases"
    elif "difference" in circuit_status:
        circuit_line = "Circuit differences."
        circuit_label = "Circuits: differences found"
    else:
        circuit_line = "Circuit result: inconclusive."
        circuit_label = "Circuits: not established"
    findings = evidence["findings"]
    if state == "invalid":
        headline = ["Invalid observations —", "comparison unavailable."]
    elif state == "failed":
        headline = ["Execution failed —", "comparison unavailable."]
    elif state != "complete" or summary == "incomplete":
        headline = ["Comparison incomplete."] + ([findings[0]["title"] + "."] if findings else [])
    elif summary == "difference":
        headline = [circuit_line] + [f["title"] + "." for f in findings[:1] if f["kind"] != "circuit"]
    else:
        headline = ["No differences", "on declared inputs."]

    shot_rows = []
    for shots in evidence["coverage"]["shot_requests"]:
        row = {"requested": shots, "reference": set(), "target": set()}
        for e in executions:
            if e["requested_shots"] != shots:
                continue
            for side in ("reference", "target"):
                c = by_id.get(f"shots-request/{side}/{e['id']}")
                if c and c["observed"] is not None and c["status"] in ("pass", "difference"):
                    row[side].add(c["observed"])
        for side in ("reference", "target"):
            row[side] = ", ".join(f"{v:,}" for v in sorted(row[side])) or "not recorded"
        row["reference_changed"] = row["reference"] != f"{shots:,}"
        row["target_changed"] = row["target"] != f"{shots:,}"
        shot_rows.append(row)

    cases = []
    seen = set()
    for e in executions:
        key = (e["graph_id"], e["angle_id"])
        if key in seen:
            continue
        seen.add(key)
        group = [x for x in executions if (x["graph_id"], x["angle_id"]) == key]
        circ = [by_id.get(f"circuit/{x['id']}") for x in group]
        prob = [by_id.get(f"probability/{x['id']}") for x in group]
        exo = [by_id.get(f"exact-objective/{x['id']}") for x in group]
        cases.append({
            "graph_id": e["graph_id"], "angle_id": e["angle_id"], "theta": e["theta"], "edges": e["edges"],
            "n": len(e["nodes"]),
            "circuit": circ[0],
            "circuit_ids": sorted({c["circuit_result_id"] for c in circ if c and c["circuit_result_id"]}),
            "prob": max((c["metric"] for c in prob if c and c["metric"] is not None), default=None),
            "prob_status": _worst(prob),
            "exo": max((c["metric"] for c in exo if c and c["metric"] is not None), default=None),
            "exo_status": _worst(exo),
            "executions": [x["id"] for x in group],
        })

    kinds = {}
    for c in checks:
        kinds.setdefault(c["kind"], []).append(c)
    kind_rows = [{"kind": k, "checks": v, "counts": {s: sum(1 for c in v if c["status"] == s)
                                                       for s in ("pass", "difference", "inconclusive", "unsupported", "error")}}
                 for k, v in kinds.items()]

    ref_src = (out / "artifacts/inputs/reference.py").read_text(encoding="utf-8")
    tgt_src = (out / "artifacts/inputs/target.py").read_text(encoding="utf-8")
    hunks = _hunks(ref_src, tgt_src)
    prov = evidence["provenance"]
    unique_circuits = len(evidence["circuit_results"])
    return {
        "e": evidence, "sha": evidence_sha, "prov": prov, "case": evidence["case"]["definition"],
        "headline": headline, "circuit_label": circuit_label, "shot_rows": shot_rows, "cases": cases,
        "kind_rows": kind_rows, "findings": findings, "by_id": by_id, "hunks": hunks,
        "ref_src": ref_src, "tgt_src": tgt_src,
        "ref_license": (out / "artifacts/inputs/reference-LICENSE.txt").read_text(encoding="utf-8"),
        "unique_circuits": unique_circuits,
        "artifacts": evidence["artifacts"],
        "receipts": prov["source_receipts"],
        "proposal": prov.get("proposal"),
        "coverage": evidence["coverage"],
        "n_exec": len(executions),
    }


def _worst(rows):
    order = ["error", "unsupported", "inconclusive", "difference", "pass"]
    statuses = {c["status"] for c in rows if c}
    for s in order:
        if s in statuses:
            return s
    return "inconclusive"


def _hunks(a: str, b: str):
    lines = list(difflib.unified_diff(a.splitlines(), b.splitlines(), "reference.py", "target.py", lineterm="", n=2))
    hunks, current = [], None
    for line in lines[2:]:
        if line.startswith("@@"):
            current = {"header": line, "lines": []}
            hunks.append(current)
        elif current is not None:
            kind = "add" if line.startswith("+") else "del" if line.startswith("-") else "ctx"
            current["lines"].append({"kind": kind, "text": line})
    hunks.sort(key=lambda h: 0 if any("shots" in l["text"] for l in h["lines"] if l["kind"] != "ctx") else 1)
    return hunks


def _env():
    loader = jinja2.PackageLoader("qref", "templates")
    env = jinja2.Environment(loader=loader, autoescape=True, undefined=jinja2.StrictUndefined,
                             trim_blocks=True, lstrip_blocks=True)
    env.filters["short"] = lambda s: (s or "")[:12]
    env.filters["num"] = lambda v: "—" if v is None else f"{v:.3g}"
    env.filters["js"] = lambda v: json.dumps(v, sort_keys=True)
    return env


def renderer_sha256() -> str:
    h = hashlib.sha256()
    for name in ("report.py",):
        h.update(Path(__file__).with_name(name).read_bytes())
    for name in ("report.html.j2", "report.css"):
        h.update(resources.files("qref").joinpath("templates", name).read_bytes())
    return h.hexdigest()


def write_export(out: Path) -> None:
    """Render index.html and manifest.json into a bundle directory that holds evidence.json + artifacts."""
    evidence_bytes = (out / "evidence.json").read_bytes()
    evidence = contracts.load_json_bytes(evidence_bytes)
    contracts.validate("evidence", evidence)
    _check_artifacts(out, evidence)
    evidence_sha = contracts.sha256_bytes(evidence_bytes)
    css = resources.files("qref").joinpath("templates", "report.css").read_text(encoding="utf-8")
    css_hash = base64.b64encode(hashlib.sha256(css.encode("utf-8")).digest()).decode()
    html = _env().get_template("report.html.j2").render(css=css, css_hash=css_hash, **_view(out, evidence, evidence_sha))
    (out / "index.html").write_text(html, encoding="utf-8")
    files = []
    for path in sorted(out.rglob("*")):
        if path.is_file() and path.name != "manifest.json":
            rel = path.relative_to(out).as_posix()
            files.append({"path": rel, "size": path.stat().st_size, "sha256": contracts.sha256_file(path)})
    manifest = {"schema": "qref.manifest/v1", "evidence_sha256": evidence_sha, "rendered_at": contracts.utc_now(),
                "renderer_sha256": renderer_sha256(), "files": files}
    contracts.validate("manifest", manifest)
    (out / "manifest.json").write_bytes(contracts.record_bytes(manifest))


def _check_artifacts(root: Path, evidence: dict) -> None:
    for a in evidence["artifacts"]:
        path = _safe(root, a["path"])
        if not path.is_file():
            raise contracts.ContractError(f"evidence artifact missing: {a['path']}")
        data = path.read_bytes()
        if len(data) != a["size"] or contracts.sha256_bytes(data) != a["sha256"]:
            raise contracts.ContractError(f"evidence artifact changed: {a['path']}")


def _safe(root: Path, rel: str) -> Path:
    p = PurePosixPath(rel)
    if p.is_absolute() or "\\" in rel or any(part in ("..", ".", "") for part in rel.split("/")):
        raise contracts.ContractError(f"unsafe path: {rel}")
    return root.joinpath(*p.parts)


def verify_bundle(root: Path) -> dict:
    """Check that a directory agrees with its manifest and that evidence links resolve. Returns the manifest."""
    if not (root / "manifest.json").is_file():
        raise contracts.ContractError("manifest.json missing")
    manifest = contracts.load_json_bytes((root / "manifest.json").read_bytes())
    contracts.validate("manifest", manifest)
    declared = {}
    for f in manifest["files"]:
        if f["path"] in declared:
            raise contracts.ContractError(f"duplicate manifest path: {f['path']}")
        declared[f["path"]] = f
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise contracts.ContractError(f"symlink not allowed: {path.relative_to(root)}")
        if path.is_file() and path.name != "manifest.json":
            actual.add(path.relative_to(root).as_posix())
    if actual - set(declared):
        raise contracts.ContractError(f"undeclared files: {sorted(actual - set(declared))[:5]}")
    if set(declared) - actual:
        raise contracts.ContractError(f"missing files: {sorted(set(declared) - actual)[:5]}")
    for rel, f in declared.items():
        data = _safe(root, rel).read_bytes()
        if len(data) != f["size"] or contracts.sha256_bytes(data) != f["sha256"]:
            raise contracts.ContractError(f"file changed: {rel}")
    evidence_bytes = (root / "evidence.json").read_bytes()
    if contracts.sha256_bytes(evidence_bytes) != manifest["evidence_sha256"]:
        raise contracts.ContractError("evidence digest does not match the manifest")
    evidence = contracts.load_json_bytes(evidence_bytes)
    contracts.validate("evidence", evidence)
    _check_artifacts(root, evidence)
    template = contracts.load_json_bytes((root / "review-template.json").read_bytes())
    if template.get("evidence_sha256") != manifest["evidence_sha256"]:
        raise contracts.ContractError("review template is bound to different evidence")
    return manifest


def rerender(run: Path, out: Path) -> None:
    """`qref report`: verify an existing bundle, copy its evidence to a new directory and render again."""
    verify_bundle(run)
    out.mkdir(parents=True, exist_ok=False)
    for path in run.rglob("*"):
        rel = path.relative_to(run)
        if path.is_file() and rel.as_posix() not in GENERATED:
            (out / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, out / rel)
    write_export(out)
    verify_bundle(out)

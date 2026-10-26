"""Render a finding-first HTML report from verified evidence and verify export bundles.

Imports no quantum library and never executes candidate code.
"""
from __future__ import annotations

import base64
import difflib
import hashlib
import json
import shutil
import zipfile
from importlib import resources
from pathlib import Path, PurePosixPath

import jinja2

from . import contracts

GENERATED = ("index.html", "manifest.json", "evidence.zip")
ZIP_NAME = "evidence.zip"
ZIP_MAX_MEMBERS = 1024
ZIP_MAX_MEMBER = 32 * 1024 * 1024
ZIP_MAX_TOTAL = 256 * 1024 * 1024


DECISION_LABELS = {"accepted_intentional": "Accepted as intentional", "rejected": "Change rejected",
                   "needs_review": "Needs review"}


def load_decisions(data: bytes, evidence: dict, evidence_sha: str) -> dict:
    """Validate a qref.decisions/v1 overlay against exact evidence bytes. Returns finding id -> recorded decision."""
    overlay = contracts.load_json_bytes(data)
    contracts.validate("decisions", overlay)
    if overlay["evidence_sha256"] != evidence_sha:
        raise contracts.ContractError("decisions are bound to different evidence (evidence_sha256 mismatch)")
    findings = {f["id"] for f in evidence["findings"]}
    recorded = {}
    for d in overlay["decisions"]:
        fid = d["finding_id"]
        if fid in recorded or fid in {r for r in recorded}:
            raise contracts.ContractError(f"duplicate decision for finding {fid}")
        if fid not in findings:
            raise contracts.ContractError(f"decision for unknown finding {fid}; only valid differences can be reviewed")
        fields = [d["reviewer"], d["reason"], d["recorded_at"]]
        if all(v is None for v in fields):
            if d["decision"] != "needs_review":
                raise contracts.ContractError(f"{fid}: a {d['decision']} decision needs reviewer, reason and recorded_at")
            recorded[fid] = None  # unfilled template entry: not recorded
            continue
        if any(v is None or not str(v).strip() for v in fields):
            raise contracts.ContractError(f"{fid}: reviewer, reason and recorded_at must all be filled in")
        if not contracts.is_utc_timestamp(d["recorded_at"]):
            raise contracts.ContractError(f"{fid}: recorded_at must be an RFC 3339 UTC time such as 2026-10-25T22:10:00Z")
        recorded[fid] = d
    return recorded


def _review(evidence: dict, decisions: dict | None) -> dict:
    findings = evidence["findings"]
    complete = evidence["run_state"] == "complete" and evidence["evidence_summary"] != "incomplete"
    labels = {}
    for f in findings:
        d = (decisions or {}).get(f["id"])
        labels[f["id"]] = {"label": DECISION_LABELS[d["decision"]] if d else "Not recorded", "record": d}
    states = [r["record"]["decision"] if r["record"] else None for r in labels.values()]
    if decisions is None and findings:
        summary = "Human decision: not recorded"
    elif "rejected" in states:
        summary = "Human review: changes rejected"
    elif not complete or any(s in (None, "needs_review") for s in states):
        summary = "Human review: pending"
    elif findings:
        summary = "Human review: recorded acceptance"
    else:
        summary = "Human review: not required"
    return {"labels": labels, "summary": summary, "has_overlay": decisions is not None}


def _view(out: Path, evidence: dict, evidence_sha: str, decisions: dict | None = None) -> dict:
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
        "review": _review(evidence, decisions),
        "origin": evidence["case"]["definition"]["origin"],
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
    decisions = None
    decisions_sha = None
    if (out / "decisions.json").is_file():
        data = (out / "decisions.json").read_bytes()
        decisions = load_decisions(data, evidence, evidence_sha)
        decisions_sha = contracts.sha256_bytes(data)
    css = resources.files("qref").joinpath("templates", "report.css").read_text(encoding="utf-8")
    css_hash = base64.b64encode(hashlib.sha256(css.encode("utf-8")).digest()).decode()
    html = _env().get_template("report.html.j2").render(
        css=css, css_hash=css_hash, **_view(out, evidence, evidence_sha, decisions))
    (out / "index.html").write_text(html, encoding="utf-8")
    files = []
    for path in sorted(out.rglob("*")):
        if path.is_file() and path.name != "manifest.json" and path.relative_to(out).as_posix() != ZIP_NAME:
            rel = path.relative_to(out).as_posix()
            files.append({"path": rel, "size": path.stat().st_size, "sha256": contracts.sha256_file(path)})
    manifest = {"schema": "qref.manifest/v1", "evidence_sha256": evidence_sha, "rendered_at": contracts.utc_now(),
                "renderer_sha256": renderer_sha256(), "files": files}
    if decisions_sha:
        manifest["decisions_sha256"] = decisions_sha
    contracts.validate("manifest", manifest)
    (out / "manifest.json").write_bytes(contracts.record_bytes(manifest))
    _write_zip(out, [f["path"] for f in files] + ["manifest.json"])


def _write_zip(out: Path, names: list[str]) -> None:
    """Generated last; contains every manifest file plus the manifest, never itself."""
    tmp = out / (ZIP_NAME + ".tmp")
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name in sorted(names):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, (out / name).read_bytes())
    tmp.replace(out / ZIP_NAME)


def _verify_zip(root: Path, declared: set[str]) -> None:
    """Check every ZIP member against the verified directory without extracting anything."""
    path = root / ZIP_NAME
    if not path.is_file():
        raise contracts.ContractError("evidence.zip missing")
    try:
        with zipfile.ZipFile(path) as z:
            infos = z.infolist()
            if len(infos) > ZIP_MAX_MEMBERS:
                raise contracts.ContractError("evidence.zip has too many members")
            names = [i.filename for i in infos]
            if len(names) != len(set(names)):
                raise contracts.ContractError("evidence.zip has duplicate member names")
            expected = declared | {"manifest.json"}
            if set(names) != expected:
                extra, missing = sorted(set(names) - expected), sorted(expected - set(names))
                raise contracts.ContractError(f"evidence.zip members differ from the manifest: extra {extra[:3]}, missing {missing[:3]}")
            total = 0
            for info in infos:
                _safe(root, info.filename)
                if info.is_dir() or info.flag_bits & 0x1 or info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                    raise contracts.ContractError(f"evidence.zip member not allowed: {info.filename}")
                if (info.external_attr >> 16) & 0o170000 == 0o120000:
                    raise contracts.ContractError(f"evidence.zip contains a link: {info.filename}")
                h, size = hashlib.sha256(), 0
                with z.open(info) as member:
                    while chunk := member.read(65536):
                        size += len(chunk)
                        total += len(chunk)
                        if size > ZIP_MAX_MEMBER or total > ZIP_MAX_TOTAL:
                            raise contracts.ContractError("evidence.zip exceeds the resource limit")
                        h.update(chunk)
                if h.hexdigest() != contracts.sha256_file(root / info.filename):
                    raise contracts.ContractError(f"evidence.zip member differs from the directory: {info.filename}")
    except zipfile.BadZipFile as exc:
        raise contracts.ContractError(f"evidence.zip is not a valid ZIP: {exc}") from exc


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
        if path.is_file() and path.name != "manifest.json" and path.relative_to(root).as_posix() != ZIP_NAME:
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
    has_decisions = (root / "decisions.json").is_file()
    if has_decisions != ("decisions_sha256" in manifest):
        raise contracts.ContractError("decisions.json and the manifest's decisions digest disagree")
    if has_decisions:
        data = (root / "decisions.json").read_bytes()
        if contracts.sha256_bytes(data) != manifest["decisions_sha256"]:
            raise contracts.ContractError("decisions.json does not match the manifest")
        load_decisions(data, evidence, manifest["evidence_sha256"])
    _verify_zip(root, set(declared))
    return manifest


def rerender(run: Path, out: Path, decisions: Path | None = None) -> None:
    """`qref report`: verify an existing bundle, copy it to a new directory, optionally attach a human
    decision overlay, and render again. Evidence bytes never change."""
    verify_bundle(run)
    if decisions is not None:
        evidence_bytes = (run / "evidence.json").read_bytes()
        load_decisions(decisions.read_bytes(), contracts.load_json_bytes(evidence_bytes),
                       contracts.sha256_bytes(evidence_bytes))
    out.mkdir(parents=True, exist_ok=False)
    skip = set(GENERATED) | ({"decisions.json"} if decisions is not None else set())
    for path in run.rglob("*"):
        rel = path.relative_to(run)
        if path.is_file() and rel.as_posix() not in skip:
            (out / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, out / rel)
    if decisions is not None:
        shutil.copyfile(decisions, out / "decisions.json")
    write_export(out)
    verify_bundle(out)

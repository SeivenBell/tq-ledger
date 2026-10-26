"""Pure comparison policy: independent interpretation, check slots, findings and run state.

Nothing here imports quantum libraries or candidate code. Inputs are recorded observations.
"""
from __future__ import annotations

import math

TOLERANCE = 1e-10
STATUSES = ("pass", "difference", "inconclusive", "unsupported", "error")
SIDES = ("reference", "target")

QCEC_MAP = {
    "equivalent": ("pass", "equal"),
    "equivalent_up_to_global_phase": ("pass", "equal"),
    "not_equivalent": ("difference", "circuit_not_equivalent"),
    "equivalent_up_to_phase": ("inconclusive", "checker_unknown"),
    "probably_equivalent": ("inconclusive", "checker_probable"),
    "probably_not_equivalent": ("inconclusive", "checker_probable"),
    "no_information": ("inconclusive", "checker_no_information"),
}

BLOCKED = {
    "failed": ("inconclusive", None),
    "incomplete": ("inconclusive", "worker_interrupted"),
    "not_run": ("inconclusive", "not_run"),
    "unsupported": ("unsupported", None),
}


def negative_cut(k: int, edges) -> int:
    """Independent declared rule. Bit i of k is qubit/node i (Qiskit count strings: bit 0 rightmost)."""
    return -sum(((k >> u) & 1) != ((k >> v) & 1) for u, v in edges)


def decode_counts(counts: dict, n: int, edges) -> float:
    total = 0
    weighted = 0
    for bits, count in counts.items():
        if len(bits) != n or set(bits) - {"0", "1"}:
            raise ValueError(f"count key {bits!r} is not a {n}-bit string")
        weighted += negative_cut(int(bits, 2), edges) * count
        total += count
    return weighted / total


def exact_objective(probabilities, edges) -> float:
    return sum(p * negative_cut(k, edges) for k, p in enumerate(probabilities))


def _check(id_, kind, scope, status, reason, summary, expected=None, observed=None, metric=None,
           tolerance=None, refs=(), circuit_result_id=None):
    return {
        "id": id_, "kind": kind, "scope_ids": list(scope), "required": True, "status": status,
        "reason_code": reason, "summary": summary, "expected": expected, "observed": observed,
        "metric": metric, "tolerance": tolerance, "artifact_refs": list(refs),
        "circuit_result_id": circuit_result_id,
    }


def _close(id_, kind, scope, expected, observed, what, mismatch_code="numeric_mismatch", refs=()):
    if expected is None or observed is None or not (math.isfinite(expected) and math.isfinite(observed)):
        return _check(id_, kind, scope, "error", "invalid_observation", f"{what}: missing or non-finite value",
                      expected, observed, refs=refs)
    diff = abs(expected - observed)
    ok = diff <= TOLERANCE
    return _check(id_, kind, scope, "pass" if ok else "difference", "equal" if ok else mismatch_code,
                  f"{what}: {'agree' if ok else 'differ'} (|Δ| = {diff:.3g})", expected, observed, diff,
                  TOLERANCE, refs)


def _blocked(rec, side):
    """Status for a check blocked by one side's execution state, or None if the side completed."""
    if rec is None:
        return ("inconclusive", "missing_prerequisite", f"{side}: no observation")
    if rec["state"] == "completed":
        return None
    status, reason = BLOCKED[rec["state"]]
    return (status, rec.get("reason_code") or reason or "worker_failed", f"{side}: execution {rec['state']}")


def build(expected, docs, circuit_results, side_failures):
    """Return (checks, findings, run_state, evidence_summary, status_counts, coverage).

    docs: side -> observation doc or None. circuit_results: execution id -> circuit result dict or None.
    side_failures: side -> reason code for a worker/environment failure, or None.
    """
    checks = []
    graphs = {}
    for e in expected:
        graphs.setdefault(e["graph_id"], e)
    recs = {}
    pairing_problems = []
    for side in SIDES:
        doc = docs.get(side)
        by_id = {}
        if doc is not None:
            for rec in doc["executions"]:
                if rec["id"] in by_id:
                    pairing_problems.append(f"{side}: duplicate execution {rec['id']}")
                by_id[rec["id"]] = rec
            expected_ids = {e["id"] for e in expected}
            unknown = set(by_id) - expected_ids
            if unknown:
                pairing_problems.append(f"{side}: unknown executions {sorted(unknown)}")
            for e in expected:
                rec = by_id.get(e["id"])
                if rec is not None and rec["input_sha256"] != e["input_sha256"]:
                    pairing_problems.append(f"{side}: input digest mismatch for {e['id']}")
        recs[side] = by_id
    if pairing_problems:
        checks.append(_check("pairing", "pairing", ["all"], "error", "input_binding_mismatch",
                             "; ".join(pairing_problems)))
    else:
        checks.append(_check("pairing", "pairing", ["all"], "pass", "equal",
                             f"{len(expected)} expected executions per side, paired by input digest"))

    # Classical basis behavior per side and graph.
    for side in SIDES:
        doc = docs.get(side)
        tables = {t["graph_id"]: t for t in (doc or {}).get("classical_tables", [])}
        for gid, e in graphs.items():
            cid = f"classical-basis/{side}/{gid}"
            table = tables.get(gid)
            if table is None:
                checks.append(_check(cid, "classical-basis", [side, gid], "inconclusive",
                                     side_failures.get(side) or "missing_prerequisite",
                                     f"{side}: basis table for {gid} not recorded"))
                continue
            bad = []
            for row in table["rows"]:
                want = negative_cut(row["k"], e["edges"])
                if row["maxcut_obj"] != want or abs(row["compute_expectation"] - want) > TOLERANCE:
                    bad.append(row["k"])
            status = "difference" if bad else "pass"
            checks.append(_check(
                cid, "classical-basis", [side, gid], status, "classical_rule_mismatch" if bad else "equal",
                f"{side}: {len(table['rows']) - len(bad)}/{len(table['rows'])} basis assignments match the "
                f"independent negative-cut rule", expected="negative_maxcut", observed={"mismatched_k": bad[:16]},
                metric=len(bad)))

    completed_pairs = 0
    any_failed = False
    for e in expected:
        eid = e["id"]
        n = len(e["nodes"])
        r = {side: recs[side].get(eid) for side in SIDES}
        blocks = {side: _blocked(r[side], side) for side in SIDES}
        for side in SIDES:
            if r[side] is not None and r[side]["state"] == "failed":
                any_failed = True
        both = all(b is None for b in blocks.values())
        completed_pairs += both

        # Per-side checks.
        for side in SIDES:
            rec = r[side]
            b = blocks[side]
            ids = {
                "shots-integrity": f"shots-integrity/{side}/{eid}",
                "shots-request": f"shots-request/{side}/{eid}",
                "returned-objective": f"returned-objective/{side}/{eid}",
                "classical-weighting-counts": f"classical-weighting/{side}/{eid}/counts",
                "classical-weighting-exact": f"classical-weighting/{side}/{eid}/exact",
            }
            if b is not None:
                for kind, cid in ids.items():
                    status, reason, why = b
                    checks.append(_check(cid, kind.split("-counts")[0].split("-exact")[0], [side, eid],
                                         status, reason, why))
                continue
            s = rec["sampling"]
            num = rec["numeric"]
            integrity_ok = (s["completed_shots"] == s["count_sum"] and s["count_sum"] > 0
                            and all(len(k) == n and not set(k) - {"0", "1"} and v >= 0 for k, v in s["counts"].items()))
            checks.append(_check(
                ids["shots-integrity"], "shots-integrity", [side, eid], "pass" if integrity_ok else "error",
                "equal" if integrity_ok else "invalid_sampling",
                f"{side}: completed shots {s['completed_shots']} vs count sum {s['count_sum']}",
                s["completed_shots"], s["count_sum"], refs=[]))
            if not integrity_ok:
                for kind in ("shots-request", "returned-objective", "classical-weighting-counts", "classical-weighting-exact"):
                    checks.append(_check(ids[kind], kind.split("-counts")[0].split("-exact")[0], [side, eid],
                                         "inconclusive", "missing_prerequisite", f"{side}: sampling data invalid"))
                continue
            honored = s["completed_shots"] == s["requested_shots"]
            checks.append(_check(
                ids["shots-request"], "shots-request", [side, eid], "pass" if honored else "difference",
                "equal" if honored else "shots_request_mismatch",
                f"{side}: requested {s['requested_shots']}, completed {s['completed_shots']}",
                s["requested_shots"], s["completed_shots"]))
            decoded = decode_counts(s["counts"], n, e["edges"])
            checks.append(_close(ids["returned-objective"], "returned-objective", [side, eid], decoded,
                                 num["returned"], f"{side}: returned objective vs independent decoding of its own counts"))
            checks.append(_close(ids["classical-weighting-counts"], "classical-weighting", [side, eid], decoded,
                                 num["module_on_counts"], f"{side}: module weighting of captured counts"))
            checks.append(_close(ids["classical-weighting-exact"], "classical-weighting", [side, eid],
                                 exact_objective(num["probabilities"], e["edges"]), num["module_on_probabilities"],
                                 f"{side}: module weighting of exact probabilities"))

        # Paired checks.
        cr = circuit_results.get(eid)
        if not both:
            reason = next(b for b in blocks.values() if b is not None)
            for kind in ("circuit", "measurement", "probability", "exact-objective", "shots-preservation"):
                checks.append(_check(f"{kind}/{eid}", kind, [eid], reason[0], reason[1], reason[2]))
            continue
        ref, tgt = r["reference"], r["target"]
        if cr is None:
            checks.append(_check(f"circuit/{eid}", "circuit", [eid], "inconclusive", "checker_budget_exhausted",
                                 "circuit check not run within the checker budget"))
        else:
            status, reason = cr["status"], cr["reason_code"]
            checks.append(_check(f"circuit/{eid}", "circuit", [eid], status, reason,
                                 f"submitted circuits: {cr['criterion'] or reason}", "equivalent", cr["criterion"],
                                 circuit_result_id=cr["id"]))
        checks.append(_check(f"measurement/{eid}", "measurement", [eid], "pass", "equal",
                             "both sides: terminal identity measurement, one classical register of width n",
                             ref["circuit"]["measurement_map"], tgt["circuit"]["measurement_map"]))
        rp, tp = ref["numeric"]["probabilities"], tgt["numeric"]["probabilities"]
        if len(rp) != len(tp):
            checks.append(_check(f"probability/{eid}", "probability", [eid], "error", "invalid_observation",
                                 "probability vectors have different dimensions"))
        else:
            diff = max(abs(a - b) for a, b in zip(rp, tp))
            ok = diff <= TOLERANCE
            checks.append(_check(f"probability/{eid}", "probability", [eid], "pass" if ok else "difference",
                                 "equal" if ok else "numeric_mismatch",
                                 f"ideal output distributions: max |Δp| = {diff:.3g}", metric=diff, tolerance=TOLERANCE))
        checks.append(_close(f"exact-objective/{eid}", "exact-objective", [eid],
                             exact_objective(rp, e["edges"]), exact_objective(tp, e["edges"]),
                             "independent exact objective, reference vs target"))
        rs, ts = ref["sampling"]["completed_shots"], tgt["sampling"]["completed_shots"]
        checks.append(_check(f"shots-preservation/{eid}", "shots-preservation", [eid],
                             "pass" if rs == ts else "difference", "equal" if rs == ts else "shots_preservation_mismatch",
                             f"completed shots: reference {rs}, target {ts}", rs, ts))

    counts = {s: 0 for s in STATUSES}
    for c in checks:
        counts[c["status"]] += 1

    invalid = any(c["status"] == "error" and c["reason_code"] in ("input_binding_mismatch", "invalid_sampling", "invalid_observation")
                  for c in checks)
    infra_error = any(c["status"] == "error" for c in checks)
    if invalid:
        run_state = "invalid"
    elif completed_pairs == 0 and (any_failed or any(side_failures.values())):
        run_state = "failed"
    elif completed_pairs < len(expected) or infra_error:
        run_state = "partial"
    else:
        run_state = "complete"
    if run_state != "complete" or counts["inconclusive"] or counts["unsupported"] or counts["error"]:
        summary = "incomplete"
    elif counts["difference"]:
        summary = "difference"
    else:
        summary = "consistent"

    findings = group_findings(checks)
    coverage = {
        "expected_executions": [e["id"] for e in expected],
        "completed_pairs": completed_pairs,
        "observed": {side: sorted(eid for eid, rec in recs[side].items() if rec["state"] == "completed") for side in SIDES},
        "missing": {side: sorted({e["id"] for e in expected} - {eid for eid, rec in recs[side].items() if rec["state"] == "completed"})
                    for side in SIDES},
        "graphs": len(graphs),
        "angle_settings": len({e["angle_id"] for e in expected}),
        "shot_requests": sorted({e["requested_shots"] for e in expected}, reverse=True),
        "not_checked": ["optimizer convergence", "hardware execution", "noise models", "dynamic circuits",
                        "inputs outside the declared graphs and angles", "whole-program equivalence"],
    }
    return checks, findings, run_state, summary, counts, coverage


FINDING_TEXT = {
    "shot_policy": ("Shot setting changed",
                    "Requested and completed shot counts differ for at least one side, or the two sides complete "
                    "different numbers of shots. This changes sampling uncertainty even when circuits are equivalent."),
    "circuit": ("Submitted circuits differ", "The checker reports the actually submitted circuits as not equivalent."),
    "probability": ("Ideal output distribution differs", "Exact output probabilities differ beyond tolerance."),
    "exact-objective": ("Exact objective differs", "Independently computed exact objectives differ beyond tolerance."),
    "classical-basis": ("Classical helper disagrees with the declared rule",
                        "A module helper disagrees with the independent negative-cut rule on at least one basis assignment."),
    "classical-weighting": ("Expectation weighting disagrees",
                            "The module's expectation differs from independent weighting of the same counts or probabilities."),
    "returned-objective": ("Returned value disagrees with its own counts",
                           "The returned objective differs from independent decoding of the histogram captured in the same call."),
}


def group_findings(checks):
    groups = {}
    for c in checks:
        if c["status"] != "difference":
            continue
        fid = "shot_policy" if c["kind"] in ("shots-request", "shots-preservation") else c["kind"]
        g = groups.setdefault(fid, {"check_ids": [], "scope_ids": set()})
        g["check_ids"].append(c["id"])
        g["scope_ids"].update(s for s in c["scope_ids"] if "/" in s)
    findings = []
    for fid, g in groups.items():
        title, explanation = FINDING_TEXT[fid]
        if fid == "shot_policy":
            changed = any(cid.startswith("shots-preservation/") for cid in g["check_ids"])
            sides = sorted({cid.split("/")[1] for cid in g["check_ids"] if cid.startswith("shots-request/")})
            if changed:
                title = "Shot setting changed"
                explanation = ("The reference and target complete different numbers of shots for the same request. "
                               "This changes sampling uncertainty even when circuits are equivalent.")
            else:
                title = "Requested shot count not honoured"
                explanation = (f"The {' and '.join(sides)} complete{'s' if len(sides) == 1 else ''} a different number "
                               "of shots than requested. Both sides agree, so the port preserves this behaviour; "
                               "whether the request should be honoured is a review decision.")
        findings.append({"id": fid, "kind": fid, "check_ids": g["check_ids"], "scope_ids": sorted(g["scope_ids"]),
                         "title": title, "explanation": explanation, "proposal_claim_refs": []})
    order = ["circuit", "probability", "exact-objective", "classical-basis", "returned-objective",
             "classical-weighting", "shot_policy"]
    findings.sort(key=lambda f: order.index(f["id"]))
    return findings

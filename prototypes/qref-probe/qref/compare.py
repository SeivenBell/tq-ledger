"""QRef referee: compare a legacy trace against a port trace.

usage: python qref/compare.py LEGACY.json PORT.json LEGACY.replay.json PORT.replay.json
exit code 0 = PASS, 1 = FAIL
Tier 1 (circuit behaviour): circuits paired by submission order.
  static pair  -> exact TVD of ideal clbit distributions, FAIL if > 1e-9
  dynamic pair -> chi-square homogeneity on referee counts (20k shots each);
                  FAIL if p < alpha/m (Bonferroni) AND TVD > 0.02
Tier 2 (observable outputs): numeric tokens of stdout under --replay (ideal counts),
  must match to 1e-9 when every circuit was replayable; advisory otherwise.
"""
import json
import re
import sys

import numpy as np
from scipy.stats import chi2_contingency

EXACT_TOL = 1e-9
ALPHA = 1e-3
TVD_MIN_EFFECT = 0.02
NUM = re.compile(r"-?\d+\.?\d*(?:e-?\d+)?")


def tvd(p, q):
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def norm(counts):
    s = sum(counts.values())
    return {k: v / s for k, v in counts.items()}


def chi2_p(a, b):
    keys = sorted(set(a) | set(b))
    table = np.array([[a.get(k, 0) for k in keys], [b.get(k, 0) for k in keys]])
    table = table[:, table.sum(axis=0) > 0]
    if table.shape[1] < 2:
        return 1.0
    return float(chi2_contingency(table)[1])


def top_diff(p, q, n=3):
    keys = set(p) | set(q)
    d = sorted(keys, key=lambda k: -abs(p.get(k, 0) - q.get(k, 0)))[:n]
    return ", ".join(f"{k}: {p.get(k, 0):.3f}->{q.get(k, 0):.3f}" for k in d)


def main():
    L, P, LR, PR = (json.load(open(f)) for f in sys.argv[1:5])
    fails, notes = [], []
    print(f"legacy  {L['script']} (qiskit {L['qiskit']}), {len(L['circuits'])} circuits")
    print(f"port    {P['script']} (qiskit {P['qiskit']}), {len(P['circuits'])} circuits")
    for t in (L, P):
        if t["error"]:
            fails.append(f"{t['script']} crashed: {t['error']}")
    lc, pc = L["circuits"], P["circuits"]
    if len(lc) != len(pc):
        fails.append(f"circuit count differs: {len(lc)} vs {len(pc)}")
    m = max(1, min(len(lc), len(pc)))
    bad = []
    for a, b in zip(lc, pc):
        i = a["index"]
        if a["static"] and b["static"]:
            d = tvd(a["exact"], b["exact"])
            ok = d <= EXACT_TOL
            how = f"exact TVD={d:.3g}"
            if not ok:
                how += f" [{top_diff(a['exact'], b['exact'])}]"
        else:
            pa, pb = norm(a["ref_counts"]), norm(b["ref_counts"])
            d, p = tvd(pa, pb), chi2_p(a["ref_counts"], b["ref_counts"])
            ok = not (p < ALPHA / m and d > TVD_MIN_EFFECT)
            how = f"sampled TVD={d:.3g} chi2 p={p:.3g} (dynamic circuit)"
            if not ok:
                how += f" [{top_diff(pa, pb)}]"
        if a["ops"] != b["ops"]:
            notes.append(f"circuit {i}: op mix changed {a['ops']} -> {b['ops']}")
        if not ok:
            bad.append((i, how))
    for i, how in bad[:5]:
        fails.append(f"circuit {i}: behaviour differs, {how}")
    if len(bad) > 5:
        fails.append(f"... {len(bad) - 5} more circuits differ ({len(bad)}/{m} total)")
    # diagnosis: does a failing port circuit reproduce some *other* legacy circuit?
    for i, _ in bad[:5]:
        b = pc[i]
        if not b["static"]:
            continue
        hits = [a["index"] for a in lc if a["static"] and tvd(a["exact"], b["exact"]) <= 1e-6]
        if hits:
            notes.append(f"port circuit {i} == legacy circuit(s) {hits}: binding/ordering permutation?")
    # Tier 2
    lnum, pnum = NUM.findall(LR["stdout"]), NUM.findall(PR["stdout"])
    deterministic = all(c["static"] for c in LR["circuits"] + PR["circuits"])
    tol = 1e-9 if deterministic else 0.02
    out_ok = len(lnum) == len(pnum) and all(
        abs(float(x) - float(y)) <= tol * max(1.0, abs(float(x))) for x, y in zip(lnum, pnum)
    )
    if not out_ok:
        diff = [
            (ll, pp)
            for ll, pp in zip(LR["stdout"].splitlines(), PR["stdout"].splitlines())
            if ll != pp
        ]
        msg = f"replayed stdout differs ({'deterministic' if deterministic else 'advisory'}): {diff[:3]}"
        (fails if deterministic else notes).append(msg)
    verdict = "FAIL" if fails else "PASS"
    print(f"tier1 circuits: {m - len(bad)}/{m} equivalent; tier2 outputs: "
          f"{'match' if out_ok else 'MISMATCH'} ({'exact replay' if deterministic else 'advisory'})")
    for f in fails:
        print("  FAIL:", f)
    for n in notes[:6]:
        print("  note:", n)
    print("VERDICT:", verdict)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

# Planning integration evidence (2026-10-23)

This record verifies the research handoff and backup probe, **not** a built Ledger application. Fact-check and red-team source reading are recorded separately in [demo-fact-check](demo-fact-check.md) and [plan-red-team](plan-red-team.md); their historical proposed fixes are superseded by current build docs.

## Actual smoke run

Executed `bash run_all.sh` from `/tmp/qref-probe`, then executed the **delivered repository source** from a disposable copy with symlinks to the installed legacy/modern environments. The latter exercised current `prototypes/qref-probe/run_all.sh`, `qref/*.py` and all cases. It did not reinstall packages or test clean-machine provisioning. Temporary copy removed.

Python subprocess returned0; checked all trace `error=` values were `None` and compared the full ordered verdict sequence with the expected sequence:

| Case | Variant | Observed |
|---|---|---|
| GHZ | port | PASS |
| GHZ | planted postprocessing endian error | FAIL |
| GHZ | planted measurement-map error | FAIL |
| GHZ | alternative seed | PASS |
| QAOA | planted parameter-order error | FAIL |
| QAOA | fixed port | PASS |
| QAOA | planted half-angle error | FAIL |
| Teleportation | port | PASS |
| Teleportation | planted swapped corrections | FAIL |
| Teleportation | equivalent deferred measurement | PASS |
| Teleportation | alternative seed | PASS |

**11 comparisons:6 expected passes,5 planted failures; all expected verdicts matched.** Earlier13/13 was a counting error. This does not estimate unseeded agent-migration error prevalence, general correctness or novelty. Installed versions: Qiskit0.46.3/Aer0.14.2 and Qiskit2.6.1/Aer0.18.0. Delivered setup script now pins those versions; clean installation was not rerun.

## Independently rerun arithmetic

Executed Python numeric expressions and `scipy.stats.beta.ppf`:

| Expression | Observed result | Scope limit |
|---|---:|---|
| `44+65/1` |109M| Litinski formula, single key |
| `44+65/11` |49.90909M| Amortized per key, k=11; limit44M |
| `1162*1684161/0.99809` |1,960,740,095.58| Retry-adjusted proxy under authors' success convention |
| `1425*2.1e6` |2,992,500,000| Product of Google's low-gate upper bounds |
| `100*(1-1960740095.58/2992500000)` |34.47819%| Contextual arithmetic only; no physical or formal dominance claim |
| `12.07*9.1/24` |4.57654days| Printed Gidney multiplier |
| `12.07*9.2/24` |4.62683days| Matches printed4.63; conclusion unaffected |
| `111/360960` |0.0003075133| Submitter-reported input counts, not reproduced circuit failures |
| CP95 binomial interval |[0.0002529801,0.0003703137]| Conditional independent-binomial model; no cross-distribution verdict |
| `1280+131+7*18` |1537| Gidney layout including idle hot patches, not Table5 width |

## Handoff and tracker checks

Checked 65 local Markdown links across the current README, agent instructions, briefing, decision memo, build documents and this evidence record: no missing files. No unfilled result placeholders were found in the current handoff. The six demo narration segments total 212 whitespace-delimited words. The build schedule sums to 12.00 focused hours; this is an allocation, not measured feasibility or a success probability. Settings parse as JSON; `/bin/bash -n prototypes/qref-probe/run_all.sh` succeeds.

Read the actual GitHub dependency endpoints for all 13 build/review issues, checked for cycles and confirmed each transitively reaches the open human project-choice issue. T1b is separate from T1 so draft-schema acceptance can unblock T2 before human publication review; T3 waits for T1b. Issue bodies mirror current PLAN. No product ticket is marked complete.

## Research spot checks

Parent read the complete PostQuantumSecurity.org tracker page and Jaques' main explanation/2025/2026 updates. These confirm the free sourced catalogue and request for an assumptions taxonomy. This proves an existing workflow and competitor, **not** demand for our implementation. Paper/source read depths remain attached to the underlying research reports.

## What remains unverified

- Ledger application, reviewed seed JSON, extractor API execution, comparison accuracy, UI, public deployment, live cost/latency and submission: **not implemented/exercised in this planning task**.
- User adoption, time savings, willingness to pay and contest odds: **not established**.
- Original cloud-session full reports: not recovered. Practitioner report is an independent local replacement; circuit-discovery file preserves the user-supplied bottom line only.
- Original cloud GitHub write authorization: still blocked in those sessions. Local authenticated publishing works and is distinct from cloud proxy authorization.

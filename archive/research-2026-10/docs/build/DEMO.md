# Demo recording plan — conditional on a real build

Archived script for the unbuilt Ledger proposal. The [current decision memo](../decision/ranked-memo.md) supersedes that recommendation. This is not the recording plan for a selected project. Use it only if Ledger is explicitly approved in [the project-choice issue](https://github.com/SeivenBell/tq-ledger/issues/14).

## Recording prerequisites

Record only working, deployed screens, with the address bar visible. Deploy early; freeze and date the reviewed dataset. The six operating-point cards are EF-893; GOOG-ZK-PA low-qubit and low-gate separately; LIT23 single-key and amortized k=11 separately; and G25 physical full attack. G25 must distinguish its Table 5 logical count from layout logical qubits and physical resources; never merge those counts. A source can yield several draft cards.

Before recording, save an actual source-grounded CLI extraction and review/export output, source/version/hash, model/prompt identifiers, timestamp and check outcomes. Publish a static evidence view or open the real exported artifact in the recording; do not imply that a writable web reviewer exists. Render's filesystem is not durable storage. If no funded key/run exists, omit the extraction segment and explicitly say extraction was not demonstrated; do not simulate it.

## Spoken script (under 240 words; approximately two minutes)

| Time | Real screen/action required | Narration |
|---|---|---|
| 0:00–0:20 | Reviewed cards with prominent scope/layer labels | “Eight hundred ninety-three logical qubits for one point addition is not a physical machine that breaks a key. Quantum cost claims describe different layers: a logical circuit, a logical full attack, or a physical architecture.” |
| 0:20–0:45 | Compare EF-893 with GOOG-ZK-PA low-qubit; click evidence for interface, inclusions and statistic/bound | “Q-Day Ledger makes those distinctions visible. Even these two point-addition records do not justify a clean savings ratio: input interfaces, lookup accounting and measured versus bounded costs need checking. Each reason links to its source. The 893 circuit's wider tests are submitter-reported, not independently reproduced.” |
| 0:45–1:00 | LIT23 single-key and k=11 operating points with formula source | “Even one paper has several operating points. Litinski reports 109 million Toffolis for one key. At eleven parallel instances, the formula gives about 49.9 million per key. Neither is a physical-qubit count.” |
| 1:00–1:30 | Actual recorded CLI output/export or deployed static run evidence; show the actual outcome | “Here is a recorded extraction from a pinned source. The model proposes a list of drafts. Code checks strict source spans and unambiguous numbers. Those checks do not prove the interpretation: a person must review scope, assumptions and counting conventions before export.” |
| 1:30–1:45 | Static run evidence and limitations | “We report actual check outcomes, including disagreements. Three development examples and three independently human-labelled held-back pairs are a small demonstration, not a statistically strong benchmark.” |
| 1:45–2:00 | Method/user panel and live URL | “The intended user is a post-quantum analyst or security writer; a possible buyer is their research or security team. Demand is unvalidated. We test whether cited refusals save review work, not predict Q-Day.” |

## Truth and cut rules

- Show the extraction's actual accepted, rejected, ambiguous or missing fields. Never preordain a rejection, successful export, correctness score or model failure. Human review/export may be CLI plus a reviewed Git change, not live web approval.
- Show cost and latency only from the actual run log, with model, date, units and measurement boundary. If unmeasured, label “not measured”; never say “a minute later” without a measurement.
- Strict span/number checks certify literal support only. Fuzzy search may help find text but never certifies it. No claim of semantic truth, independent circuit verification, or exhaustive source coverage.
- Optional baseline: same source access and tasks for the LLM; record model/prompt, raw answers, independent labels and n. If no funded key, state not run; never invent a result.
- Do not put the 34.5% calculation in the core demo. If asked: it is a limited retry-adjusted Q×T calculation against Google's low-gate upper bound, with unresolved inclusion/interface comparability; not physical savings. The “more than 50%” figure originates in the ECDSA.Fail authors' abstract, not only the press.
- No headline parser, authentication, memory, CI sophistication or live writable review is required. Cut narration about missing screens instead of staging them.

## Evidence depth and competitive context

This plan relies on [claims-classic.md](../research/build/claims-classic.md), [claims-2026.md](../research/build/claims-2026.md) and [span-check-feasibility.md](../research/build/span-check-feasibility.md), not independently reproduced circuits. [practitioner-pain.md §7](../research/practitioner-pain.md#7-sources) records full/partial reading depth and limitations. The fact-check and red-team findings are incorporated into these recording constraints; source spans still require builder/human re-anchoring.

The free [PostQuantumSecurity.org tracker](https://www.postquantumsecurity.org/trackers/qubit-estimates.html) already lists sourced estimates and assumptions. Do not claim the first or only ledger. The proposed distinction—precise evidence plus reasoned refusal—remains an unvalidated usefulness hypothesis.

Contract detail: the card IDs are `EF-893`, `GOOG-ZK-PA-LOW-Q`, `GOOG-ZK-PA-LOW-G`, `LIT23-SINGLE`, `LIT23-K11` and `G25-RSA2048`. Show ratios only for fully comparable, exact, unbounded values; caveats/bounds get no ratio. A missing funded key means extraction is `not_run` and full AI-workflow acceptance is unmet—not a substitute success. The shortened recording above must disclose that limitation.

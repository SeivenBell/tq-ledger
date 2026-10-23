# Build North decision memo: a narrow claim-comparison tool, conditionally

Status: research synthesis, updated 2026-10-23. **Recommendation, not Severyn's final decision.** [Choose the project to build](https://github.com/SeivenBell/tq-ledger/issues/14) remains open. The build contract is in [PRODUCT](../build/PRODUCT.md), [ARCHITECTURE](../build/ARCHITECTURE.md) and [PLAN](../build/PLAN.md).

## Bottom line

- **Recommend Q-Day Ledger only as a source-linked comparison/refusal workbench, not another qubit tracker.** Target user: a PQC analyst or resource-estimate curator explaining what a new claim actually counts. Ivezic performs this work publicly; Jaques asks for a more precise taxonomy of physical assumptions. Neither has agreed to use our tool.
- The [new free PostQuantumSecurity.org tracker](https://www.postquantumsecurity.org/trackers/qubit-estimates.html) already has 11 sourced RSA/ECC rows, assumptions, runtimes and a CC BY CSV. This weakens the original recommendation: ledger **32 → 30/45**, down one competition and one adoption point. Quotes, operating points and explicit reasons not to compare are the incremental hypothesis; demand is not validated.
- **QRef is a credible separate backup**, with a runnable two-runtime referee. Integration rerun: 11 comparisons, 6 expected passes and 5 planted failures, all matched. No unseeded migration-error rate or real maintainer adoption was measured. Its screen score is 31, so the Ledger is not an arithmetic runaway winner.
- **Do not build an arena or generic investor-research agent.** ECDSA.Fail/Yukon and public `uncompute` already cover discovery evaluation; diligence/intelligence is crowded. The interesting paper is an input, not a product requirement.
- The earlier 20-card, 14-pair, live-extraction/auth/memory plan was too large. Recommend six reviewed operating-point cards, three development examples, three human-labelled held-back comparisons, one source-grounded extraction run and a deployed read-only evidence UI. No inferred physical savings, arbitrary paper ingestion or autonomous scientific verdicts.
- There is no defensible numerical probability of winning. The controllable acceptance criteria are a useful comparison, correct source labels, actual run evidence, a stable live link and a comprehensible two-minute video.

## Evidence and what it does not establish

| Evidence | Read depth / record | Decision implication |
|---|---|---|
| [Ivezic's 893-qubit analysis](https://postquantum.com/security-pqc/ecdsa-fail-low-qubit-circuit/), Oct 14/17 | Full; [practitioner report](../research/practitioner-pain.md), [fact check](../research/build/demo-fact-check.md) | A named analyst manually separates subroutine, input-interface and architecture assumptions. No measured time saving or commitment to our app. |
| [Jaques, Quantum Landscape](https://sam-jaques.appspot.com/quantum_landscape), 2025/2026 updates | Partial: main explanation and both updates; practitioner report §7 | Wants a precise assumption taxonomy; also an incumbent and possible collaborator. No address or consent invented. |
| [PQS tracker](https://www.postquantumsecurity.org/trackers/qubit-estimates.html), launched Oct 21 | Full page and CSV; practitioner report §7 | Static catalogue is already served. Prefer complementary, exportable evidence/refusals. |
| Unitary Foundation 2025 survey | Partial aggregate CSV sections; full summary, practitioner report §7 | Price/docs/tools/compatibility dominate broad practitioner responses. Claim comparison is specialist pain, not the field's biggest daily problem. |
| [ECDSA.Fail paper v2](https://arxiv.org/html/2609.09582v2), Sept 19 | Full in fact-check audit; earlier synthesis read benchmark/results partially | Q×T, coherent/classical inputs, success treatment and bound conventions matter. Quotes alone do not certify correctness. |
| [Gu et al.](https://arxiv.org/pdf/2610.22367), Oct 2026 | Methods/results and SI read in source audits; [field report](../research/field-needs.md) and fact check | Public evaluator/artifacts exist; search compute and complete harness accounting are not reproduced here. Do not equate input-distribution-specific failure experiments. |
| [QRef probe](../research/build/qref-probe.md) | Code executed locally; 11 comparisons observed | Small-core feasibility, not evidence that real agent migrations frequently fail or that novelty is established. Abstract-only prior-art leads cannot establish novelty. |

## Screening scores, not probabilities

Nine 1–5 criteria: U observed user pain for this artifact; A AI contribution; S Severyn's advantage; B complete weekend build; J judge appeal; P adoption path; C competitive openness; G credibility in AI and quantum; R low risk. These are subjective screening judgments [INFERENCE], not measured outcomes. User value and credibility outrank competition odds per the research brief. No user commitment means U≤4. Historical scores below were not all rerun after the small feasibility probes.

| Numeric order | Narrow candidate | U | A | S | B | J | P | C | G | R | Total |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | QRef migration referee | 3 | 3 | 4 | 2 | 3 | 3 | 4 | 4 | 5 | 31 |
| 2= | Q-Day comparison/refusal workbench | 4 | 4 | 4 | 3 | 3 | 3 | 2 | 4 | 3 | 30 |
| 2= | SRQC readiness map | 3 | 4 | 4 | 3 | 3 | 3 | 3 | 4 | 3 | 30 |
| 4 | Not Yet use-case triage | 3 | 4 | 4 | 3 | 3 | 2 | 2 | 4 | 4 | 29 |
| 5 | Independent reversible-circuit re-grader | 2 | 2 | 4 | 4 | 2 | 2 | 3 | 4 | 5 | 28 |
| 6= | Calibration-agent benchmark | 2 | 3 | 3 | 3 | 3 | 2 | 2 | 4 | 5 | 27 |
| 6= | Verified QEC lab agent | 2 | 3 | 4 | 4 | 2 | 2 | 2 | 4 | 4 | 27 |
| 8= | PQC evidence pack | 3 | 3 | 2 | 3 | 4 | 3 | 2 | 2 | 4 | 26 |
| 8= | General subroutine-cost registry | 2 | 3 | 4 | 3 | 2 | 2 | 2 | 4 | 4 | 26 |
| 10= | Reproducible circuit-search service | 2 | 4 | 4 | 2 | 2 | 2 | 1 | 4 | 3 | 24 |
| 10= | TQ arena (superseded premise) | 1 | 4 | 4 | 3 | 2 | 1 | 1 | 4 | 4 | 24 |
| 12 | Materials-novelty audit | 3 | 2 | 2 | 2 | 3 | 2 | 2 | 2 | 5 | 23 |
| 13= | Investor diligence agent | 2 | 2 | 2 | 3 | 2 | 1 | 1 | 1 | 3 | 17 |
| 13= | Quantum diligence portal | 2 | 2 | 2 | 3 | 2 | 1 | 1 | 1 | 3 | 17 |

QRef's B=2 was a pre-probe caution about the entire product, not its now-runnable referee. Do not silently raise its total from a planted-case demonstration. Ledger is the conditional recommendation because U and A are stronger under the agreed priority, not because 30 exceeds 31. A maintainer asking for QRef on an actual migration could reverse the recommendation. SRQC has funding-program relevance but no applicant asking for this dashboard; a program call is not a customer.

## Red team and deciding tests

| Option | Strongest reason not to build it | Cheap deciding evidence |
|---|---|---|
| Ledger | Free tracker and expert prose already suffice; semantic review dominates extraction savings | Send one source-linked refusal to Ivezic/Jaques or the tracker maintainer. Ask for the next actual comparison and whether they would reuse/export it. No reply means unvalidated, not rejected. |
| QRef | Planted bugs are easy; real ports may work, and application-specific observables defeat generality | Run one genuine agent migration outside the planted suite; compare independent observables and ask a maintainer whether the evidence helps review. Do not claim a rate from one example. |
| SRQC | DOE/DARPA need full-stack work and institutional teams, not a stand-alone literature map | Show one accurately scoped target/estimate card to an applicant; ask whether it enters an existing workflow. No procurement claim without a user. |

## Recommended one-page build contract

**Job:** select two curated resource claims; show what each counts, its quote/version and operating point; answer whether a specific numerical comparison is supported. If units, scope or input interfaces conflict, explain the conflict. If assumptions are missing, return **insufficient evidence**, not a made-up incompatibility or ratio.

**Corpus:** six reviewed operating-point records: EF-893; Google point-addition low-qubit and low-gate; Litinski single-key and amortized k=11; one Gidney full-attack physical record. Logical and physical numbers remain separately typed. Gidney's Table5 logical width and layout width must not be merged. EF holdout failures are submitter-reported, not independently reproduced.

**AI:** a model drafts a list of typed claims from allowlisted, pinned text. Code checks exact canonical spans, unambiguous number tokens and explicitly encoded arithmetic. A person reviews semantic labels. Source content is untrusted data; no arbitrary URL fetch, tool instructions or circuit execution. Output is a read-only draft plus downloadable review/export; no ephemeral-server approval database.

**Proof:** three development comparisons plus three independently human-labelled held-back comparisons. Show counts and individual disagreements. Extraction evaluation checks field/value/operating-point mapping, false accepts and false rejects; provenance success is not truth. A same-model, same-source-access JSON baseline is fairer than a knowledge-cutoff quiz. If a funded API key is unavailable, record that missing prerequisite; do not advertise an unrun AI workflow.

**Usability:** two cards, plain-language reasons, clickable source evidence, unknowns visible, no jargon-first home strip or unsupported headline percentages. Show actual extraction run metadata and cost/latency only after execution. Deploy early; record by Sunday afternoon; preserve a submission buffer.

**Deliberate exclusions:** general search/arena, physical-resource conversion, attack circuits, arbitrary PDFs, ongoing news monitoring, writable auth, memory and partner integrations until the core is complete. Clerk/SurrealDB can be honest extensions only when exercised. **Eon Era is not a fit** for the custom dataset; Expo is unnecessary.

**Resources:** CPU app and a small funded API budget, independent of pending hackathon credit. [Build feasibility](../research/build/build-feasibility.md) records official-doc read depth and API constraints, including Citations/structured-output incompatibility. Model pricing is a dated planning input, not a bill. Cloud-session subscription credits cannot be assumed to fund API calls.

## Corrections and research provenance

- `quantum-ai-discovery.md` originally asserted no evaluator was released. Corrected: [`andigu/uncompute`](https://github.com/andigu/uncompute), Apache-2.0, exists. The arena premise is withdrawn.
- `field-needs.md` originally said DARPA IV&V deadline Oct15. Corrected to **Dec30,2026**, [official opportunity](https://www.darpa.mil/work-with-us/opportunities/darpa-pa-26-02-01), full read in prior synthesis. This still does not validate an app buyer.
- Fuzzy provenance and flattened-exponent guessing were proposed after an exploratory span probe. **Rejected** after red-team review. See [span experiment and limits](../research/build/span-check-feasibility.md).
- Litinski's asymptotic per-key limit is **44M**, not50M; k=11 gives about49.9M and single-key109M. 34.5% is contextual retry-adjusted Q×T arithmetic versus Google's low-gate bound, not a general improvement result. Primary source locations and read depths: [fact check](../research/build/demo-fact-check.md).
- The cloud practitioner report could not be pushed; [practitioner-pain.md](../research/practitioner-pain.md) is an independent local re-research, not the recovered original. [ai-circuit-discovery.md](../research/ai-circuit-discovery.md) preserves the supplied bottom line, not its unavailable full evidence. No further paid recovery runs are required for this planning decision.

Next human decision: approve this narrow build or choose QRef. No product implementation or outreach has been silently approved by this memo.

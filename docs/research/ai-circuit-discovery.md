# AI circuit discovery: what is open and what is already served

Recovery and reconciliation: October 23, 2026. This is the current synthesis for the circuit-discovery ticket. The [complete original Fable report](originals/ai-circuit-discovery-fable.md) is preserved unchanged, not replaced by its earlier chat summary.

## Bottom line

- **An outsider can use public tools; access is not the main opening.** The Apache-2.0 `andigu/uncompute` evaluator exists. The earlier claim that the paper released no evaluator was wrong. That does not make a complete search effort cheap or reproducible within 12 hours.
- **Do not build another arena.** Existing evaluators and ECDSA.Fail/Yukon already serve this job. The original report's participant counts, model lists and third-party performance claims remain dated, attributed findings—not newly reproduced results.
- **The verification concern is real but the proposed gap was overstated.** The ECDSA paper already reevaluates 42 circuits on 50,000 common inputs. A blanket claim that independent regrading is absent is false.
- **The narrower request is regression and approximation disclosure.** Public issues ask to retain known failing inputs and make the evidence behind accepted approximate circuits visible. A maintainer-compatible contribution is more credible than a new certification service.
- **This is not our default AI-first build.** Simulation and explicit test policy do the checking; the material role for an LLM is weak. Source rights, organizer policy and a recipient's actual next task remain prerequisites.
- **The original report was delivered in chat, not pushed by its cloud session.** We have the full text. Its claimed commit `071a72e` and reported grader experiments were not independently recovered. Local publication of the text is separate from fixing that cloud session's authorization.

## What the original report contributed

The original analysis distinguishes public search access from a useful product. It examines the released evaluator, existing challenges, search systems, performance claims and sampled-grader failure modes. It recommends an independent regrading service rather than another leaderboard.

Its full method notes, source register, candidate variants and subjective scores remain in the [archived original](originals/ai-circuit-discovery-fable.md). Its claimed timing and mutation experiments are attributed to that agent. This recovery pass did not rerun them, inspect its temporary patch/bundle, or obtain the original git commit.

The earlier summary repeated strong claims about third-party improvements and certification. Those claims should not stand alone as current verified facts. Current decisions use the source-specific qualifications below and the [new claim-workflow investigation](round2/claim-workflows.md).

## What the newer evidence changes

### Regrading already exists

The [ECDSA.Fail paper, v2](https://arxiv.org/html/2609.09582v2), dated September 19, 2026, describes a common-input reevaluation in §5.4. Read depth in the new investigation: partial—benchmark methods §§3.1–3.3, comparison/results §5.1 and reevaluation/reproduction §§5.4–5.5, plus limitations. No circuits were rerun in that investigation.

This weakens a new service whose differentiator is simply “we test the circuits independently.” It does not mean the present reporting is sufficient or that every result is correct.

### Participants ask for a more specific improvement

[Issue 239](https://github.com/Layr-Labs/ecdsafail-challenge/issues/239), September 8, 2026, asks to retain a known failing input and make approximation evidence easier to inspect. [Issue 284](https://github.com/Layr-Labs/ecdsafail-challenge/issues/284), September 9, repeats the documentation concern. Read depth: both issue bodies full; the single comment on issue 284 was not read in the source investigation. The parent also read issue 239's body. Its reported Rust experiment was not independently run.

Passing sampled tests is not universal correctness. Conversely, one counterexample does not automatically violate a policy that permits approximation. An honest report separates official status, known failures, test distribution, fresh observations and policy. It does not issue an unrestricted “correct” certificate.

### Existing claim infrastructure is more developed than the old vision document

The current HashSmash README, paired-review documentation and Pareto contract describe typed claims, evidence, review lanes and experiments. The new investigation read those documents in full. It inspected only part of the live page and did not execute the pipeline. Published code, configured admission requirements and actual live operation are distinct evidence levels.

The old vision document's “harness TBD” language is not a reliable description of the current implementation. A new evidence-review site needs a concrete missing task, not a claim that these components do not exist.

## The useful contribution, if a recipient wants it

[INFERENCE] A bounded contribution could package one published regression witness and a readable baseline appendix for an existing challenge. Inputs would be a pinned circuit identity, permitted public fixture and an organizer-approved test policy. Outputs would show official acceptance separately from regression observations and their limits.

This is not a solver, circuit-improvement service, nonce search or alternative official leaderboard. A signed receipt would establish who ran what, not scientific correctness. A failure-rate interval would need a stated sampling model; a targeted counterexample corpus is not automatically an independent random sample.

Before selecting it, confirm:

1. A maintainer still wants the specific report or regression contribution.
2. Applicable file licences and the protected-infrastructure boundary permit the proposed reuse and integration.
3. The fixed example runs within the available CPU/time budget. Fast evaluation of a small task does not establish the cost of a large fresh corpus or full search.
4. The result adds something not already provided by existing reevaluation and participant tools.

No inquiry was sent. Outreach is paused. Without these answers, this remains a contribution hypothesis, not a validated product or a promised 12-hour certification service.

## Reading and provenance

All recovery and new-source checks are dated October 23, 2026.

| Material | Actual evidence depth |
|---|---|
| [Original full report](originals/ai-circuit-discovery-fable.md) | Full user-supplied text read and preserved. Source-reading claims and experiments remain attributed unless independently checked elsewhere. Its exact original commit was not retrieved. |
| Public `andigu/uncompute` release | Repository existence and Apache-2.0 release are independently recorded in the earlier local source audits. Original Fable analysis describes contract/evaluator inspection. No grader execution in this reconciliation pass. |
| [Current claim-workflow report](round2/claim-workflows.md) | Full synthesis read; its register lists exact dates/depths for ECDSA methods/results, current HashSmash documents, terms and issue bodies. It reports no runtime reproduction. |
| [Existing demo source audit](build/demo-fact-check.md) | Prior primary-source audit supplies paper/table and input-distribution qualifications. It does not independently reproduce the original Fable experiments or certify participant circuit claims. |

The [current decision memo](../decision/ranked-memo.md) withdraws the previous Ledger recommendation and compares this contribution with quantum upgrade review, CODECHECK assistance and battery-data work. It keeps the final choice with Severyn.

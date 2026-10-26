# Which project should we build?

Updated October 23, 2026, after four parallel source investigations and a real notebook-upgrade experiment.

This file compares different jobs we could help people do. It is not a list of app names. The previous Ledger recommendation is withdrawn. No final project has been selected; that remains [Severyn's decision](https://github.com/SeivenBell/tq-ledger/issues/14).

Recommendations, relative priorities and proposed build scopes below are `[INFERENCE]`. They are not observed adoption or delivery results.

## Bottom line

**For the AI × quantum hackathon, my provisional pick is a small quantum-code upgrade reviewer, built around existing QCEC checks.** It would show what an AI-generated port preserved, what changed and what was not checked. It should be an open-source review aid, not a new circuit verifier or a claim that we certify scientific correctness.

That is the strongest technical fit we have exercised, not a validated market. No practitioner has agreed to use it. Our normal coding-agent baseline already explained the change in the real example; the additional value is confirming that explanation by execution and making the evidence easy to review.

Under our usefulness-first priority, BDF has the strongest explicit request in this shortlist. The quantum reviewer ranks first on the AI/quantum fit we have exercised, not on demonstrated user demand. None currently satisfies every criterion. CODECHECK has an existing review workflow, but we need a real task from a reviewer before choosing a product scope.

We should not build another claim tracker, circuit arena or general reproduction platform. The existing alternatives cover substantially more than the earlier memo acknowledged. There is no defensible probability of winning, and none of these options is established as the optimal solution.

## What changed the decision

| New finding | Consequence |
|---|---|
| The complete original practitioner report recommends verified SDK migration, not Ledger | The two original reports were not joint support for our previous pick. Both texts are now preserved; their original commits and reported experiments are not independently recovered. |
| The free PQS tracker already has sourced resource estimates, assumptions, runtimes and CSV export | A catalogue is not an opening. We found no inspected request for our proposed two-card refusal website. |
| HashSmash already documents typed claims, evidence and paired reviews; the ECDSA paper already regrades 42 circuits on 50,000 common inputs | “Nobody does evidence review or independent regrading” is not a valid premise. Published code, configured checks and live operation still need separate labels. |
| QCEC already checks circuit equivalence, including cases our earlier account omitted | We should reuse it. The narrower question is how to review the surrounding experiment and execution settings. |
| A real QAOA port preserves all nine checked circuits but changes effective shot counts | There is a concrete review example. It is one setting change, not a measured agent error rate. The agent disclosed it. |
| CODECHECK has a funded, ongoing checking workflow; BDF has a recent explicit feature request | Contributing to existing work may be more useful than attracting users to another website. Funding and requests are not purchase commitments. |

The earlier 1–5 scores were subjective screens. They are removed from the current decision rather than adjusted until a preferred option wins.

## The distinct options

These alternatives serve different users and accept different inputs. They are not variations of a name or pitch.

| Option | User and concrete output | Existing solution and remaining gap | Decision |
|---|---|---|---|
| Quantum-code upgrade review | A researcher or reviewer gets a reproducible before/after report for a trusted local Qiskit program | IBM migration skills, ordinary coding agents and MQT QCEC already do much of the work. A combined circuit, sampling and decoded-result report may reduce manual review; that saving is unmeasured. | Best provisional hackathon fit; test usefulness before claiming a product gap. |
| CODECHECK report helper | A codechecker records a failed attempt and links it to the relevant manuscript result | codecheck-py already provides manifests, hashes, previews and certificates. We need to identify a missing recording step, not duplicate these features. | Best broader research-workflow lead, conditional on a real reviewer task. |
| Calculated battery-data columns | A BDF user adds power, capacity or energy using documented units and precedence | Maintainers/users explicitly request this; PyProBE already supplies recipes. Correct integration is useful, but a new AI app is unnecessary. | Clearest small contribution; weak fit if the challenge requires material runtime AI and quantum relevance. |
| Circuit-baseline failure disclosure | An existing benchmark shows known counterexamples separately from its official sampled result | Participants explicitly request regression retention and clearer approximation evidence. Regrading infrastructure already exists; the remaining issue may be documentation and policy. | Contribute only with organizer direction and clear reuse terms. Weak AI role; do not start a new arena. |

An unanswered question is not rejection. But it is also not evidence of adoption. Outreach is paused; no practitioner inquiry has been sent.

## What the quantum reviewer would do

### The practical problem

A program can run after an upgrade while the experiment changes. A circuit-equivalence check cannot establish that shot counts, parameter selection, result decoding and surrounding Python behavior stayed the same.

Our real example makes the distinction visible. The old QAOA helper runs 1,024 simulated measurements even when the caller asks for 512 or 17. The Sonnet port honors the caller's requested setting. QCEC reports equivalent circuits in all nine checked cases. Both facts can be true.

The port may be correcting the old program. The reviewer must choose between preserving the historical experiment and accepting that correction. The tool should expose the decision, not label every difference an AI mistake.

### A complete first version, if selected

Input: two trusted local implementations, pinned source and target environments, and a declared adapter with fixed graph, angle and shot inputs. Support one static Qiskit/Aer workflow. Do not promise arbitrary notebook revival.

Output: a downloadable report and a small read-only viewer containing:

- Source identity, dependency versions and actual run records.
- QCEC circuit verdicts, kept separate from small-input numerical checks.
- Exact probabilities and decoded objective comparisons on the declared inputs.
- Requested versus completed shots, with explicit behavior-change notes.
- A human review decision: preserve old behavior, accept an intentional change, or leave it unresolved.
- Unsupported paths and failures shown directly, including an unavailable old runtime.

AI produces the port and proposes an explanation. Separate execution records test those claims. A recorded real model run is acceptable evidence of what happened; a public UI must not pretend it makes live model calls if it only displays that record.

All Python execution stays local on inspected input. A public upload-and-execute service is outside scope. QCEC is a dependency, not our invention. Hardware, noise, dynamic circuits, optimizer convergence and whole-program equivalence remain outside the first version.

### The adoption test

The natural destination is an IBM migration example, an MQT integration/example, or a maintainer's review—not a new account-based destination site. We have not obtained acceptance from any of them.

The most useful next question, if outreach is later authorized, is: “Can you point me to one public notebook upgrade where these checks would help?” Ask for an artifact, not enthusiasm for an AI platform.

Keep this direction only if the report supplies a check the reviewer needs or demonstrably reduces review work. If a plain agent plus existing QCEC/Aer checks gives the same evidence with no extra burden, publish the example or upstream integration and stop calling it a separate product.

### A twelve-hour scope budget

This is a proposed allocation, not an observed delivery time or implementation authorization.

| Work | Hours | Completion condition |
|---|---:|---|
| Freeze the supported contract and dependencies | 2 | Both trusted versions run; unsupported inputs get explicit outcomes |
| Package the existing execution and comparison path | 3 | One command produces the full report without a model deciding pass/fail |
| Build the report viewer and export | 2 | A reader can find the changed setting, source and limits without reading code |
| Evaluate a fresh real port or alternate declared implementation | 2 | Individual results published; no planted example counted as natural failure |
| Check the actual surface, publish evidence and record the demo | 3 | Working link, reproducible local command and honest two-minute recording |
| Total | 12 | A complete bounded review workflow, not a universal verifier |

Use CPU simulation and the already working local Claude subscription path. Cloud-session credit does not fund an API-backed website. A live hosted model feature would need separately confirmed API funding; it is not part of this proposed minimum.

## When another option is better

**Choose the BDF contribution** if the goal is a small, concretely requested improvement used through an existing package. Its difficult parts are units, integration boundaries, missing values and recorded-versus-derived precedence—not multiplying two columns. It offers less direct quantum or AI-product evidence.

**Choose a CODECHECK helper** if a reviewer supplies a failed check and identifies the manual step their current tools do not cover. The project plans roughly 60 checks over two years, so there is a real workflow. That does not show they need our proposed feature. Automatic repair followed by automatic certification would also conflict with the separation between recording a check and fixing the research code.

**Choose the benchmark disclosure contribution** if an organizer wants the specific regression/disclosure artifact already requested in public issues. First resolve the protected-infrastructure and licence boundaries. Do not claim that one counterexample defeats a benchmark whose acceptance policy permits approximation.

**Reconsider Ledger only** if an analyst supplies an actual next comparison and wants a field or export missing from current tools. An exportable correction to the existing tracker is a more credible starting point than another catalogue. We do not have that request now.

## Why this could be presentable—and what is still unknown

The quantum review story is simple: **the circuit stayed the same; the experiment setting changed.** A live local rerun, visible source versions and an explicit review decision give judges something inspectable. This suits Severyn's research-software and quantum background without claiming a new discovery algorithm.

We have not demonstrated user time savings, repeated demand, a second independent migration result, a finished interface or a live deployed product. We have not proved that this would beat existing tools in a fair reviewer task. Those are limits, not reasons to manufacture a stronger demo.

For calls, keep three distinctions clear: circuit equivalence versus program behavior; historical reference versus scientifically correct behavior; and execution evidence versus proof for all inputs. Ask what the person last upgraded, what they checked manually and which report would enter their next review.

## Evidence and reading depth

All new investigations were conducted October 23, 2026. Full source registers, dates, method/results sections, reusable components and limitations are in the linked reports. No abstract-only paper drives this recommendation.

| Source | Read depth used here |
|---|---|
| [Quantum workflow investigation](../research/round2/quantum-workflows.md) | QCEC equivalence/partial-equivalence guides full; IBM migration skill partial, Phases 1–6; migration-paper methods/results read. Source register distinguishes current docs from stale survey data. |
| [QAOA notebook](https://github.com/qiskit-community/qiskit-textbook/blob/0ae905083ec3872d7ddc6bb4001d5468f476d93f/content/ch-applications/qaoa.ipynb) | Partial notebook: all code cells inspected; cell 18 helpers executed across both runtimes. Deliberately stale 2023 source, not current demand evidence. [Actual checks](../research/round2/workflow-checks.md). |
| [Claim workflow investigation](../research/round2/claim-workflows.md) | PQS page/CSV full; HashSmash current README, paired-lane and Pareto docs full, live page partial; ECDSA paper partial, benchmark methods and reevaluation/results §§3, 5.4–5.5; issues 239/284 bodies full. |
| [Scientific reproduction investigation](../research/round2/scientific-reproduction.md) | CODECHECK project/workflow full; codecheck-py relevant features partial; shortlisted papers' methods, evaluation setup and results read, with section-level depths. Released trace checked without rerunning the experiment. |
| [Scientific operations investigation](../research/round2/scientific-operations.md) | BDF issue 136 body and comments full; PyProBE recipe docs full; public fixture partial. Arithmetic only exercised in the parent check, not the package contribution. |
| [Original practitioner report](../research/originals/practitioner-pain-fable.md), [original circuit report](../research/originals/ai-circuit-discovery-fable.md) | Full supplied texts recovered from chat. Their source read-depth claims and reported experiments remain attributed unless independently checked above. Claimed original commits `21d086a` and `071a72e` were not independently recovered. |

The experiment code and raw results are preserved on [a separate research branch](https://github.com/SeivenBell/tq-ledger/tree/research/round2-qaoa-probe/prototypes/round2-qaoa), not shipped as production code on main. The old files in `docs/build/` are marked archived Ledger proposals. Existing build tickets remain blocked by the human project choice; this memo does not silently authorize a replacement build.

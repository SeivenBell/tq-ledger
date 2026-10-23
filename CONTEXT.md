# Q-Day Ledger: domain contract

Status: recommended build, not implemented. Severyn's project choice remains open in [issue #14](https://github.com/SeivenBell/tq-ledger/issues/14). `docs/build/PRODUCT.md` defines scope; `docs/build/ARCHITECTURE.md` defines interfaces; `docs/build/PLAN.md` defines T1–T12 plus human review T1b.

## Claims and evidence

- **Source**: a dated, versioned document or captured public record. Its manifest identifies the URL, version or capture time, licence, canonical-text hash, and canonicalization procedure.
- **Canonical text**: the exact UTF-8 text against which checks run. Normalization occurs once, before hashing. A later check must not silently normalize or repair a quotation.
- **Claim**: a source's statement about quantum resources under specified conditions. A source can state several claims and alternative designs.
- **Operating point**: one jointly stated design or configuration. Numbers from alternative designs must not form a synthetic design.
- **Claim card**: one operating point from one source. The core has six reviewed cards, not six independent papers. Each metric identifies its layer and semantic context.
- **Evidence anchor**: a source ID and hash, exact quoted span, half-open character offsets, and a human-readable locator. Numeric anchors also identify the complete numeric token and its offsets.
- **Provenance check**: establishes that a selected quote and numeric token occur in the pinned text. It does not establish that the field correctly describes the source.
- **Semantic review**: a person checks the field meaning, numeric mapping, context, and omissions against the source. A matching token does not replace this review.
- **Headline**: a restatement, not automatically evidence for its underlying claim. Headline parsing is optional, not part of the core demonstration.

## What a metric means

- **Target problem**: the exact problem and parameters, such as RSA-2048, ECDLP-secp256k1, or generic 256-bit ECDLP. Generic does not mean a particular named curve.
- **Scope**: the computation covered, such as point addition, modular inversion, or full key recovery. Full-attack records must disclose classical work and omitted attack stages.
- **Layer**: `logical_circuit`, `logical_algorithm`, or `physical_architecture`. Layer belongs to each metric. One card can contain logical inputs and physical outcomes without conflating them.
- **Unit**: the counted resource, such as logical qubits, physical qubits, Toffolis, CCX+CCZ, or days. No automatic logical-to-physical or T-to-Toffoli conversion exists.
- **Bound**: `exact`, `upper_inclusive`, `upper_exclusive`, `lower_inclusive`, `lower_exclusive`, `approximate`, or `not_stated`. A bound is not a cost statistic. Exact here describes the stated numeric quantity, not circuit correctness.
- **Statistic**: `peak`, `fixed_count`, `average_executed`, `expected`, or `not_stated`. An average can also have an upper bound.
- **Addend interface**: `classical`, `coherent`, `window_indexed`, `not_applicable`, or `not_stated`. These are distinct interfaces, not synonyms.
- **Inclusions**: a reviewed map of relevant costs to `included`, `excluded`, `not_applicable`, or `not_stated`. An empty map does not establish equal coverage.
- **Input distribution**: the tested or assumed inputs, their generation procedure, exclusions, and any selection of circuits or nonces. Equal sample counts do not establish equal distributions.
- **Counting convention**: a documented counting rule. An explicit CCX+CCZ convention does not license conversion from arbitrary T counts.
- **Amortization**: the number of parallel instances and whether the count is total or per key. The Litinski k=11 card is a ledger-derived operating point, not a single-key claim.
- **Runtime role**: `constraint` means a deadline used to select resources. `outcome` means a resulting runtime. Different outcomes alone are not conflicting constraints.
- **Hardware assumptions**: the error model, code, connectivity, cycle time, reaction time, and other stated assumptions behind a physical estimate.

## Correctness evidence

- **Failure budget**: the allowed failure probability, with its scope and input distribution.
- **Observed failures**: reported failures and trial count, with the test procedure and reporter. Observations are not a certified budget.
- **Submitter-reported**: evidence reported by a circuit's submitter. EF-893's 111/360,960 population test has this status.
- **Independent verification**: a named external check with its method and artefact. A public proof or evaluator report must describe what it actually checks. It does not prove universal circuit correctness.
- **Derived value**: an output from a named, fixed formula with cited inputs and explicit ledger-selected parameters. It is not an observed source value.

## Comparison rules and verdicts

A comparison selects `card_id:operating_point_id:metric_id` on each side. It evaluates nine rules:

1. Same target problem and parameters.
2. Same scope, inclusions, and relevant classical work.
3. Same metric layer.
4. Same unit and counting convention.
5. Compatible statistic, bound, and input distribution.
6. Same relevant addend interface.
7. Compatible correctness requirements and evidence.
8. Same amortization basis and instance count.
9. Compatible hardware assumptions and runtime constraints for physical metrics.

Each rule returns `pass`, `caveat`, `conflict`, `unknown`, or `not_applicable` with evidence references. Unknown evidence is not a known conflict.

- **Comparable** (`comparable`): every applicable rule passes.
- **Comparable with caveat** (`caveat`): no rule is unknown or conflicting, but a documented limitation remains.
- **Not comparable** (`not_comparable`): at least one documented conflict exists. Unknown rules remain visible alongside that conflict.
- **Insufficient evidence** (`insufficient_evidence`): a required rule is unknown and no conflict already establishes non-comparability.

No ratio appears for `not_comparable` or `insufficient_evidence`. The core also omits ratios for caveats and bounded quantities. Side-by-side upper bounds do not establish which actual circuit is smaller.

## Review and check states

Review and code checks are separate dimensions:

- `research_draft`: transcribed from the research corpus, not independently checked.
- `machine_extracted`: proposed by the extractor. This status says nothing about check success.
- `human_reviewed`: a named person approved every populated field and the explicitly unknown fields against the pinned source.
- `rejected`: a reviewer rejected the draft or field.

Each code check has `pass`, `fail`, or `not_run`, with a reason. Numeric ambiguity is a failure, not a weak pass. Missing source text produces `not_run`, not certification. Fuzzy search can locate a possible quote but cannot make a provenance check pass.

Publishing requires current passing provenance checks for observed numeric fields, valid derivations, and complete human review. Published cards can retain explicit semantic unknowns. Such unknowns can prevent comparison. Publication does not reproduce a circuit, validate a physical estimate, or certify the source's truth. No `reproduced` badge exists in this build.

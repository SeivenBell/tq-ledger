# Q-Day Ledger: product contract

Status: recommended build, 2026-10-23. No product implementation or evaluation result is claimed here. Severyn's final choice remains open in [issue #14](https://github.com/SeivenBell/tq-ledger/issues/14).

Working name: **Q-Day Ledger**. Tagline: *Quantum code-breaking claims, with receipts.*

## 1. Problem and intended user

Quantum cryptanalysis claims describe different computations. Logical qubits for one point addition are not physical qubits for a full attack. Upper bounds, measured averages, amortized per-key costs, and runtime-constrained estimates also differ.

The primary user is a PQC analyst preparing a cited assessment. The buyer hypothesis is an analyst firm or an internal risk team. Neither willingness to pay nor time saved is established. The ledger supports evidence review, not prediction of a quantum-break date or a migration recommendation.

Two source-grounded examples motivate the core:

- ECDSA.Fail submission 457ccb7a reports 893 logical qubits for a point-addition subroutine. Its 111 failures in 360,960 population-test shots are submitter-reported, not an independent correctness certificate. The source is a public submission record, not an arXiv paper.
- Litinski's title says 50 million Toffolis. The paper explicitly explains reuse across parallel instances. Its single-key count is 109 million, while `(44 + 65/k)` million per key gives about 49.9 million at k=11. The limit is 44 million, not 50 million. This is an amortization distinction, not evidence of misconduct.

Source leads: `docs/research/build/claims-classic.md`, `claims-2026.md`, and the primary URLs below. Corpus quotations are research drafts. They need fresh anchors and human review before publication.

## 2. Core deliverable

Build a small public, read-only ledger. A local command-line workflow produces extraction drafts and review exports. The deployed site shows committed cards and recorded run artefacts. It does not accept live extraction or persist reviewer edits.

1. Read six reviewed operating-point cards.
2. Select two metrics and inspect nine comparison rules.
3. Open each number's source quote, locator, version, hash, and check result.
4. Inspect one genuine model extraction run, including its actual successes, mistakes or ambiguities; no rejection is preordained.
5. Download the reviewed JSON and the recorded evaluation results.

The promise is limited: **a model proposes fields, deterministic code checks provenance, and a person reviews meaning before publication.** Neither provenance checks nor human approval prove that a scientific claim is true.

### Exact seed scope

| Card ID | Operating point | Required content and qualification |
|---|---|---|
| `EF-893` | `submission-457ccb7a` | 893 logical qubits and the reported integer average-executed Toffoli metric 2,218,127. Keep the measured mean and its rounding distinct. Record classical-addend scope, test procedure, nonce selection, and submitter-reported 111/360,960 population results. Do not call the submission a leaderboard winner. |
| `GOOG-ZK-PA-LOW-Q` | `low_qubit` | Point addition: ≤1,175 logical qubits and ≤2,700,000 CCX+CCZ under the source's stated convention. Preserve average-executed statistic separately from upper bounds. |
| `GOOG-ZK-PA-LOW-G` | `low_gate` | Point addition: ≤1,425 logical qubits and ≤2,100,000 CCX+CCZ. This is a different design, not interchangeable metrics from the low-qubit point. |
| `LIT23-SINGLE` | `single_key` | Generic 256-bit ECDLP, full-attack logical count: 109 million Toffolis per key. Record relevant classical recovery and counting conventions. Do not relabel the curve as secp256k1. |
| `LIT23-K11` | `parallel_k11` | Ledger-derived `(44 + 65/11)` million Toffolis per key, displayed as approximately 49.9 million. Cite formula coefficients and label k=11 as a selected parameter. Preserve the paper's convention and distinguish any later adjustment factors. |
| `G25-RSA2048` | `physical_layout` | One physical full-attack record with source-stated 897,864 physical qubits and 4.96-day expected runtime, subject to review of the source's assumptions. Keep Table 5's 1,399 logical qubits, text's 1,409 active logical qubits, and 1,537 layout/hot-patch/factory accounting as distinct labelled entries. Do not resolve their discrepancy by choosing one universal width. |

These six cards cover four sources. They are not six independent research results. The two Litinski cards share a formula family. The two Google cards share a paper but represent alternative designs.

Primary links:
- [EF submission](https://api.ecdsa.fail/api/submissions/457ccb7a-4436-4e8c-8e8c-f7d22c3c81b5).
- [Google paper](https://arxiv.org/abs/2603.28846). T1 must pin the inspected version, rather than trust an unversioned URL.
- [Litinski v1](https://arxiv.org/abs/2306.08585v1).
- [Gidney v1](https://arxiv.org/abs/2505.15917v1).

For Google, record window-indexed interface and the separately billed lookup from Equation (1). Hidden circuit details remain unknown. Source statements about proof support must identify their version and tested statement. The build does not independently rerun that proof.

## 3. User-visible behaviour and acceptance

| Surface | Core acceptance |
|---|---|
| Ledger `/` | Exactly six published cards, grouped by scope and metric layer. Alternative operating points are clearly named. No unlabelled qubit leaderboard. |
| Card `/cards/{id}` | Every observed number opens its exact span and complete numeric token. Show source version/capture, licence, review identity/time, code-check state, and semantic unknowns. Derived values show formula and inputs instead. |
| Compare `/compare` | Both selections specify card, operating point, and metric. Show each rule's status and evidence. Unknown evidence returns `insufficient_evidence` unless a documented conflict already establishes `not_comparable`. |
| Method `/method` | Explain canonical text, strict checks, human semantic review, limited evaluation, licence constraints, and excluded features. |
| Recorded draft `/drafts/{id}` | Render an actual saved extraction output and per-field checks. Identify it as a recorded run. No promise of a specific rejection or live review action. |
| Results `/eval` | Render saved counts, disagreements, field-mapping errors, uncertainty, model/run metadata, and baseline availability. Separate development examples from held-back results. |
| Local review/export | CLI accepts field decisions from a local decision file. It exports an approved card only after current checks and complete review. The export reaches the site through a normal git change and redeploy. |

The primary walkthrough compares EF-893 with Google's low-qubit point-addition record. It explains source-backed interface and inclusion differences, bounds, and unresolved evidence without a reduction ratio. Litinski single-key versus k=11 shows amortization. EF-893 versus G25 is only a basic target/scope/layer boundary example, not the hero comparison.

Basic accessibility is required: labelled form controls, keyboard navigation, readable contrast, and text labels for check states. A performance score or sub-two-second response target is not a submission claim without measurement.

## 4. Checks and their limits

- Pin canonical text and its hash before selecting spans. Check exact offsets without fuzzy repair.
- Select a complete numeric token inside the exact span. Reject ambiguous tokens, digit-subsequence matches, and flattened-exponent guesses.
- Keep layer, statistic, bounds, scope, inclusions, input distribution, addend interface, amortization, and hardware assumptions explicit. A human reviews categorical mappings.
- Return uncertainty when required evidence is missing. Never treat two `not_stated` values as evidence of compatibility.
- Show no ratio for mismatched scopes, unknown evidence, caveats, or bounded quantities in the core. The 34.5% calculation is not a core path.
- Provide only the fixed Litinski per-key derivation needed by the six cards. A generic formula evaluator, G25 typo detector, confidence calculator for circuit failures, and physical resource estimator are not core requirements.

Review and provenance states follow `CONTEXT.md`. A draft can pass code checks and still be semantically wrong. Published records can state unknown facts, but must not fill those facts by inference.

## 5. Small evaluation, not a benchmark claim

The core evaluation has three development comparison examples and three independently human-labelled held-back comparison pairs. Development examples are regression tests, not accuracy evidence. Severyn labels held-back pairs from source evidence after the engine and rules freeze. The implementation agent must not receive those labels before the first run.

For extraction, use one development excerpt and two held-back excerpts from different pinned sources. Each excerpt targets one or two operating points, with approximately 12–20 numeric fields across the held-back excerpts. This is an excerpt-level extraction exercise, not general full-paper accuracy. The reviewer freezes exact gold fields, meanings, and alignment identifiers before extraction runs. Existing corpus exposure and possible model pretraining contamination must be disclosed. Do not call the papers unseen.

Report raw counts and denominators for:

- Extracted values, omissions, extra fields, and ambiguous or unmatched operating points.
- Numeric correctness and semantic field-mapping correctness against human gold.
- Exact span/token check outcomes.
- False accepts: incorrect proposed fields that pass deterministic provenance checks.
- False rejects: correct proposed fields that deterministic checks reject.
- Held-back comparison verdicts and rule-level disagreements.

Show descriptive 95% Wilson intervals for rates with nonzero denominators. State that fields are clustered by source and these intervals do not establish generalization. Zero denominator means `not_applicable`, not zero error. Three held-back pairs are a demonstration, not a statistically strong benchmark.

If a funded model key is available, give the same model both comparison inputs and their source excerpts for a structured-output LLM baseline. Give neither method the human gold labels. Report the actual outcome, not an assumed chatbot failure. If funding is unavailable, report extraction and model baseline as `not_run: funded_key_unavailable`. Do not manufacture a run or claim the full AI workflow is complete.

## 6. Scope and resources

**Core, T1–T8 plus human review T1b:** schema and six reviewed cards, pinned sources, strict provenance checks, deterministic comparison, read-only pages, CLI extraction/review/export, small evaluation, early deploy, actual recorded run evidence, README, video, and submission.

**Optional, disabled by default:** T9 headline parsing, T10 authentication, T11 memory, T12 automated CI. Authentication without durable approvals does not create a review workflow. Memory must never enter held-back prompts. No optional item can consume review, deployment, recording, or submission buffer.

**Excluded:** new circuits, new attack estimates, logical-to-physical conversion, T-to-Toffoli conversion, live source monitoring, live writable review on Render, arbitrary URL ingestion, and a forecast of quantum-breaking dates.

Budget about 12 focused solo hours, including human review, integration, deployment, and recording. Coding agents can reduce typing, not remove reviewer responsibility. `PLAN.md` allocates these hours and states failure decisions. A funded model key and deployment funding are prerequisites, not assumed benefits of a pending credit request.

## 7. Licensing, independence, and risk

Only redistribute complete canonical text where the source licence permits it. The research corpus identifies Google and Gidney as CC BY, Litinski as arXiv nonexclusive, and the ECDSA.Fail hosted platform as proprietary. Recheck the exact source versions and terms before publication. Public visibility is not permission to mirror.

For restricted sources, retain private local canonical text and hashes. Publish only permitted short attributed excerpts and links after review. Any unavailable or prohibited evidence must remain unverified and unpublished until resolved. Full public reproducibility is limited when canonical text cannot be redistributed or recovered identically.

This project organizes public claims. It does not reproduce circuits or validate physical architectures. Source-grounded physical records are allowed. New physical estimation, employer code, employer data, and proprietary methods are excluded.

Evidence of usefulness remains a hypothesis until an analyst tries the workflow. Ask whether the comparison saves review effort and whether the exported evidence fits an existing assessment. Do not claim measured time savings, guaranteed correctness, or a probability of winning.

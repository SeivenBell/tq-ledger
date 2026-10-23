# Q-Day Ledger: architecture, checks, and evaluation

Status: implementation contract, 2026-10-23. The product is not implemented by this planning deliverable. Read `CONTEXT.md`, `PRODUCT.md`, and `PLAN.md` together.

## 1. Shape and implementation choices

Use Python 3.12 with `uv`, FastAPI, Jinja2, one stylesheet, and repository JSON. The public process only reads committed artefacts. No database, account system, browser model calls, writable review route, or persistent Render disk is required.

```text
pinned local source -> canonical text + manifest -> extractor -> list of drafts
                                                        -> strict checks
                                                        -> local human review
                                                        -> export -> git/redeploy
committed cards + recorded runs + eval results -> read-only public pages
```

Canonicalization, provenance, comparison, and extraction are separate modules. Callers use the interfaces below. Do not add a provider abstraction for a single model adapter.

The extractor uses the installed provider SDK's supported structured-output method. Configure an actually available model through `LEDGER_MODEL`. Do not hard-code a model or SDK method merely because a planning report named one. Record the resolved model ID and SDK version. A funded `ANTHROPIC_API_KEY` is a prerequisite for genuine model runs. Structured output constrains shape, not truth.

Use an always-on Render instance if funded. Check current pricing and service availability during setup. The plan does not promise a fixed price or that unapproved credits will arrive. Preserve the working repository outside `/tmp` before implementation, or maintain an external backup after each accepted change.

## 2. Files and data contracts

T1 owns `pyproject.toml`, `uv.lock`, and the initial `Makefile`, schema/manifests and draft seeds. T1b owns human approval of the six records after T2 checks exist; it is a separate issue so closing T1 can unblock T2 without a review/check dependency cycle. Other tickets request dependency changes through the integration owner. This prevents concurrent lockfile edits.

```text
ledger/schema.py                typed records and schema validation
ledger/sources.py               pinned fetch/canonicalization and hash checks
ledger/verify.py                exact span/token checks and fixed derivation
ledger/compare.py               deterministic nine-rule comparison
ledger/extract.py               source-grounded model proposal
ledger/review.py                local decision validation and card export
app/main.py                     read-only routes and health route
app/templates/ app/static/      rendered pages and CSS
data/sources/*.json             manifests, not unrestricted source mirrors
data/text/*.txt                 only redistributable canonical texts
.cache/sources/                 private canonical texts, gitignored
data/cards/*.json               six reviewed published records
data/drafts/*.json              publishable recorded drafts
data/runs/*.json                sanitized run metadata
data/eval/dev-pairs.json        three public development examples
data/eval/results.json          actual results rendered by the site
eval-private/                  gitignored gold, held-back inputs and labels until run freeze
scripts/extract_cards.py        source/excerpt -> draft list and run record
scripts/review_cards.py         decision file -> checked export
scripts/run_eval.py             fixed comparisons/extraction -> results
scripts/check_cards.py          offline checks over committed records
tests/                         interface-level regression tests
render.yaml                     read-only service configuration
README.md                       run, verify, provenance and limitations
```

Create files only when their ticket needs them. No scaffolding for T9–T12 belongs in the core.

### Source and evidence

`SourceManifest` contains:

- `id`, title, authors, source date, URL, and pinned version or capture timestamp.
- Licence/terms URL, redistribution decision, reviewer, and decision note.
- Acquisition URL, acquisition timestamp, raw-content hash, and canonical-text SHA-256.
- Canonicalizer ID/version, tool version, text encoding, and transformation description.
- Local cache key and optional repository text path. Public manifests must not expose private absolute paths.
- Canonical-text availability: `committed`, `local_only`, or `unavailable`.

`EvidenceAnchor` contains `source_id`, `text_sha256`, `quote`, `start`, `end`, and `locator`. All offsets are half-open Unicode code-point offsets into the complete canonical text, not byte offsets. Require `canonical_text[start:end] == quote`.

A numeric anchor adds `token_text`, `token_start`, `token_end`, and optional table row/column labels. Token offsets use the same complete canonical text. The token must be complete, inside the quote, and uniquely selected. Table labels aid human review but do not replace token checks.

### Fields, cards, and metrics

`EvidenceField[T]` contains either a stated `value` with evidence anchors, or `state=not_stated` with a review note. Do not encode unknown as an empty string, zero, false, or an empty inclusion list.

Each `ClaimCard` contains:

- `id`, `source_id`, `operating_point_id`, title, and plain-language summary.
- `metrics: dict[str, Metric]`, with stable metric IDs.
- `correctness_evidence`, separating budgets, observed tests, reporter, input procedure, selection, and independent checks.
- `review`, with status, reviewer, time, field decisions, and reviewed-content hash.
- `checks`, generated by code and tied to current content and source hashes.

Each card is one operating point. Each `Metric` contains:

| Field | Meaning |
|---|---|
| `value` | Decimal string. Never use binary floating-point equality for source numbers. |
| `unit` | Closed vocabulary including logical/physical qubits, Toffolis, CCX+CCZ, T gates, hours, days, count, probability. |
| `layer` | EvidenceField of `logical_circuit`, `logical_algorithm`, or `physical_architecture`. Never infer solely from unit or card title. |
| `bound` | `exact`, `upper_inclusive`, `upper_exclusive`, `lower_inclusive`, `lower_exclusive`, `approximate`, `not_stated`. |
| `statistic` | `peak`, `fixed_count`, `average_executed`, `expected`, `not_stated`. Bound and statistic are independent. |
| `kind` | `observed` or `derived`. Observed requires a numeric anchor. Derived requires a derivation record. |
| `context` | Evidence-backed target, scope, inclusions, counting convention, input distribution, addend interface, amortization, hardware assumptions, and runtime role. |
| `reporting` | Reporter and whether the quantity is the source's own estimate or a third-party quotation. |

Every categorical field in `context` uses `EvidenceField`. Context is explicit per metric. A helper can copy shared reviewed context during drafting, but the persisted metric must be self-contained. Metrics from Table 5 and a layout paragraph must not silently inherit equal inclusions.

Inclusions map relevant cost names to `included`, `excluded`, `not_applicable`, or `not_stated`. State the vocabulary needed by each scope: lookup, addend preparation, uncomputation, retries, classical key recovery, and factories where relevant. Completeness is a human decision, not equality of two empty maps.

Input distribution identifies sampling, exclusions, circuit-dependent generation, and selection. Amortization records `basis=total|per_key`, `instances`, and reuse conditions. Runtime role is `constraint`, `outcome`, or `not_applicable`. Required but unstated details use `not_stated`.

`Derivation` contains a fixed `formula_id`, input field references, selected parameters, Decimal precision, and display rounding. The only required formula is `litinski_per_key_v1`: `(44 + 65/k) * 1000000`. Coefficients have source anchors. k=11 is a labelled ledger choice. Preserve the unrounded result and display approximately 49.9 million. Do not mix this pre-adjustment count with later `10/9` adjustments or physical throughput estimates.

For `G25-RSA2048`, use separate metrics such as `physical_qubits`, `runtime_expected`, `logical_table5`, `logical_active_text`, and `logical_layout_text`. Keep 1,399 / 1,409 / 1,537 with their distinct context and an unresolved-source note. No default scalar `logical_qubits` may erase the distinction.

### States and publication

Review states: `research_draft`, `machine_extracted`, `human_reviewed`, `rejected`.

Check states: `pass`, `fail`, `not_run`, each with a code and explanation. Relevant codes include `source_unavailable`, `hash_mismatch`, `span_mismatch`, `token_mismatch`, `ambiguous_number`, `unsupported_number_format`, and `derivation_mismatch`.

A published card requires complete human decisions, current passing observed-number provenance checks, and valid derived metrics. A changed field, canonical hash, or evidence anchor invalidates its review. Explicit semantic unknowns are permitted after review, but cannot certify comparison. A recorded rejected draft can be public with its draft status and permitted evidence. There is no `reproduced` state or automatic approval.

## 3. Source and strict-check interfaces

```python
fetch_source(pinned_spec: SourceSpec) -> CanonicalSource
load_source(manifest: SourceManifest, cache_root: Path) -> CanonicalSource
verify_card(card: ClaimCard, sources: Mapping[str, CanonicalSource]) -> CheckReport
```

`CanonicalSource` holds the manifest and exact text. Fetch only allowlisted pinned arXiv versions or explicitly configured seed-record URLs. Do not accept arbitrary user URLs. Limit response size and time. Never execute source content.

Canonicalization decodes text, uses NFC Unicode and LF line endings, and removes HTML scaffolding before hashing. Select one textual representation for mathematical markup. Record that procedure. Do not concatenate duplicate MathML representations. For PDF-only material, record the `pdftotext -layout` version. Any manual repair creates a separately identified canonicalization revision, not a silent check-time substitution.

A missing exponent, an ambiguous table layout, or a broken conversion requires a better source representation or an explicit failed check. It does not permit guessing `1011` means `10^11`.

Numeric grammar is deliberately small:

- Complete signed integer or decimal tokens, with valid comma grouping.
- Explicit scientific notation, such as `6.5e+09`, or `1.26 × 10^11` with an explicit exponent marker.
- Explicit scale words/suffixes: thousand, million, billion, k, M, B. Support the exact documented phrases `a million` and `half a million` if used.
- Approximation and inequality markers remain separate bound metadata. The numeric magnitude must still match.

The parser must reject partial matches: 893 inside 1893, 1,399 inside 13,990, and a detached exponent digit are failures. Do not collect digits and compare subsequences. Do not fuzzy-match to certify spans. Do not evaluate free-form source expressions. A format outside the grammar returns `unsupported_number_format`.

The selected numeric token must parse to the proposed value under the documented scale convention. A numeric anchor without explicit token offsets fails when multiple candidates exist. Duplicate numbers need distinct token offsets. Do not choose the first matching number automatically. A syntactically valid token can still map to the wrong metric or design. The human checks this, and evaluation scores that error.

`verify_card` has no network or model side effects. It reports unavailable sources as `not_run`. It never turns them into passes. `scripts/check_cards.py` distinguishes a publication-blocking failure from an unavailable optional source. Public reproducibility notes must list local-only evidence.

## 4. Comparison interface and rules

```python
compare(left: MetricRef, right: MetricRef, cards: Mapping[str, ClaimCard]) -> Comparison
# MetricRef = (card_id, operating_point_id, metric_id)
# Comparison = verdict, rules[9], explanation, ratio_or_none
```

An invalid reference returns an explicit input error, not a scientific verdict. All valid references produce all applicable rule results. Each result has `status=pass|caveat|conflict|unknown|not_applicable`, reason code, explanation, and evidence references.

| Rule | Known agreement or limitation | Known conflict | Unknown evidence |
|---|---|---|---|
| R1 Target | Same problem and parameters | RSA vs ECDLP, or distinct named curves | Generic 256-bit ECDLP vs a specific curve without justified mapping |
| R2 Scope/inclusions | Same operation and reviewed relevant inclusions | Subroutine vs full attack, included vs excluded lookup/classical work | Omission or ambiguous coverage |
| R3 Layer | Same per-metric layer | Logical vs physical, or circuit vs full algorithm | Unstated layer |
| R4 Unit/convention | Same unit and evidenced counting convention | T vs Toffoli without a supported exact mapping | Unstated counting convention |
| R5 Statistic/distribution/bound | Same statistic and compatible input distribution. Different documented bounds yield a caveat only after other requirements pass. | Average vs fixed/worst-case count, or known materially different input distributions | Statistic, bound, or required distribution unspecified |
| R6 Addend | Same relevant interface. Non-point-addition scopes can be not applicable. | Classical vs coherent vs window-indexed | Required interface unstated |
| R7 Correctness | Same documented requirement and equivalent evidence basis | Explicitly different required correctness criteria | Budget vs observations alone, absent requirements, or incompatible/unknown test support |
| R8 Amortization | Same total/per-key basis, instance count, and reuse conditions | Single-key vs per-key k=11, or incompatible reuse | Instance count or basis missing |
| R9 Hardware/runtime | Same required assumptions. Documented architectural differences with otherwise aligned assumptions can be a caveat. Different runtime outcomes can be a caveat. | Different binding runtime constraints or materially conflicting hardware assumptions | Required physical assumption missing |

R9 is not applicable to logical metrics without physical claims. Compare runtime outcomes as metrics in their own right when selected, but do not confuse an outcome with a resource-selection deadline. No arbitrary 10× failure-budget rule exists.

Aggregate precedence: any `conflict` -> `not_comparable`. Otherwise any required `unknown` -> `insufficient_evidence`. Otherwise any `caveat` -> `caveat`. Otherwise -> `comparable`. Preserve unknown rows even when another rule establishes a conflict. Missing facts alone must never produce `not_comparable`.

The core permits a ratio only for `comparable`, exact unbounded numeric values, identical units, and nonzero denominator. It still labels the scope and operating points. No ratios for caveats, upper bounds, or incomplete evidence. In particular, comparing Google's two upper bounds cannot prove superiority of either hidden circuit.

The three development examples are:

1. **Primary useful comparison:** `EF-893:submission-457ccb7a:logical_qubits` versus `GOOG-ZK-PA-LOW-Q:low_qubit:logical_qubits`. Both concern logical point addition, not different cryptographic targets. Review classical versus window-indexed addend interfaces, separately billed lookup, tested input distributions, and measured values versus bounds. Show only source-backed conflicts. If required evidence remains unresolved without a known conflict, return `insufficient_evidence`. Never fabricate a reduction ratio.
2. `LIT23-SINGLE:single_key:toffoli_per_key` versus `LIT23-K11:parallel_k11:toffoli_per_key`: known amortization conflict. Other unknowns remain visible.
3. The two Google point-addition operating points, selecting their gate metrics: show upper bounds and any source-supported limitation. If required distribution or correctness equivalence is missing, use `insufficient_evidence`, not an invented comparable result. Severyn freezes the expected rule rows after source review, before implementation.

Development labels are regression requirements, not measured engine accuracy. No forced positive comparison is necessary for the demo.

EF-893 versus G25 physical qubits is only a basic target/scope/layer boundary example, not the hero comparison or an additional scored development pair. The main demonstration should emphasize the harder EF-893/Google comparison and Litinski amortization.

## 5. Extraction and local review interfaces

```python
extract(source: CanonicalSource, selection: ExcerptSelection, config: ExtractionConfig) -> ExtractionRun
# ExtractionRun contains list[DraftCard], raw structured response, checks, and run metadata.
review_export(drafts: list[DraftCard], decisions: ReviewDecisions,
              sources: Mapping[str, CanonicalSource]) -> ExportResult
```

`ExcerptSelection` uses full-text offsets. Returned quote/token offsets remain relative to the complete canonical text. A source can produce zero, one, or several drafts. Require separate operating points. Do not merge alternative rows or assume one paper means one card.

The prompt contains the schema, canonical source excerpt, and explicit instructions to quote evidence or mark unknown. It contains no gold cards, held-back labels, prior runs, or memory. Treat source text as untrusted data, not model instructions. A known source hash and approved source selection are required before a paid call.

`ExtractionConfig` names the actual model, token limit, timeout, and maximum allowed spend. The CLI requires an explicit per-run spending limit. No unbounded retry loop. A failed provider call records failure and publishes no synthetic output.

Each run records source/excerpt hashes, prompt hash, model ID, SDK version, timestamp, output and check hashes, input/output tokens if returned, latency, and cost basis. Use provider-reported or documented-price-calculated cost and label which. If unknown, record `not_available`, not zero. Remove secrets and restricted text from public logs.

`ReviewDecisions` identifies the reviewer and timestamp. It has approve/reject decisions for every populated field and acknowledgement of unknown fields. Approval re-runs strict checks against current source text. Any missing decision, rejected required field, failed check, or content/hash mismatch blocks card export. Rejected drafts remain drafts. Write the export to a local output path for normal git review. The deployed process never writes approvals to Render's filesystem.

## 6. Evaluation interface and result schema

`scripts/run_eval.py` consumes frozen gold, excerpt selections, held-back pair labels, the engine, and optional real model credentials. It writes actual results and an input-manifest hash. Do not calculate a headline percentage over development examples.

### Freeze and alignment

1. Review the six seed cards from primary evidence.
2. Use one excerpt for extraction prompt development.
3. A human prepares two held-back source excerpts, about 12–20 numeric fields total. Each excerpt targets one or two operating points.
4. The human labels each gold field with `(source_id, target, scope, operating_point_id, metric_id)` and evidence. Include categorical context.
5. Freeze prompt, schema, rules, gold, selections, and hashes before the held-back run.
6. After the engine freezes, the human independently labels three held-back pairs. Keep labels outside the implementation agent's context until the first run.
7. Run each held-back exercise once with that frozen configuration. If fixes require another run, report both attempts and mark the second as a rerun.

Independence means the human labels from source evidence without copying engine answers. It does not mean external expert validation. Papers may already occur in research notes or pretraining. Disclose that exposure. This is held-back task data, not evidence of unseen-paper generalization.

Match draft operating points by the frozen alignment tuple, not list order or a fuzzy title match. Ambiguous matches are errors. List extra claims separately. Report omissions over gold fields and extras over proposed fields. An extra supported field is not automatically false, but requires separate human review and must not improve the scored denominator.

### Required measurements

- Gold fields, proposed fields, aligned fields, missing fields, extras, and unmatched drafts.
- Numeric value/unit/bound/statistic correctness.
- Categorical context correctness and field-mapping errors, including swapped operating points, wrong row/column, and correct number assigned to wrong metric.
- Exact span pass/fail/not-run counts and numeric-token pass/fail/not-run counts.
- False accepts: human-incorrect proposed fields with passing span and token checks, divided by all human-incorrect proposed fields checked.
- False rejects: human-correct proposed fields rejected by those checks, divided by all human-correct proposed fields checked.
- Held-back pair verdict matches and every rule-level disagreement. Development results remain separate.

Also report errors among accepted fields so readers can see the publication risk. Do not score omission as a verifier false reject: the verifier cannot reject an unproposed field.

For each rate with denominator >0, report numerator, denominator, and a descriptive 95% Wilson interval. Implement this short fixed calculation with the standard library. No SciPy dependency is needed for the core. A zero denominator is `not_applicable`. State that source-clustered fields and three pairs do not justify strong statistical or market claims.

### Model baseline and saved results

If funded credentials exist, run the same available model on all three held-back pairs. Supply both selected records and the same pinned source excerpts used by the comparison exercise. Do not supply gold labels or engine verdicts. Require structured `verdict`, rule statuses, and cited evidence. Grade by the frozen human rubric. Report unknown/invalid responses as such. Use the same context budget, and disclose input or truncation differences.

If the funded key is unavailable, set `extraction.status` and `baseline.status` to `not_run`, with `funded_key_unavailable`. The deterministic core can still deploy, but the model workflow acceptance remains unmet. Do not substitute fabricated drafts or a knowledge-only chatbot test.

`data/eval/results.json` contains schema version, commit/input hashes, frozen configuration, dataset counts, exposure notes, actual run IDs, per-field results, comparison results, baseline status/results, uncertainty notes, and every disagreement. The site renders this file. Presentation numbers must come from the file, not hand-edited copy.

## 7. Public routes and operations

Required read-only routes: `/`, `/cards/{id}`, `/compare`, `/method`, `/drafts/{id}`, `/eval`, `/healthz`, and JSON downloads. The compare form accepts stable metric references, never arbitrary code or source URLs. Unknown IDs return a normal not-found or input error. Escape source quotations and model text in templates.

Render loads committed artefacts at startup. It does not fetch papers, need a model key, or run extraction. Use a funded always-on plan if available. Deploy the minimal shell early, then redeploy accepted data and pages. Do not advertise an unavailable live workflow.

`Makefile` interfaces: `run`, `test`, `verify`. `verify` invokes offline card validation and recorded-data checks. A separate explicit source-fetch command may fill the local cache. Missing nonredistributable texts must produce an availability report, not a false claim of universal public verification. Detailed CI is T12 optional.

Main integration owner runs the final checks after all ticket changes land. No ticket runs concurrent builds, tests, lint, or formatters during shared edits. The README states the commands and which checks require local-only source access.

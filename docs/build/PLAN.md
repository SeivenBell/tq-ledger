# Q-Day Ledger: bounded build plan

Status: archived Ledger plan, not an active build queue. The [current decision memo](../decision/ranked-memo.md) supersedes the previous recommendation. Severyn's [project choice](https://github.com/SeivenBell/tq-ledger/issues/14) remains open. Use these tasks only if Ledger is explicitly selected.

Submission deadline: **Oct 25, 11:59 PM ET**. Target submission: **Sunday 8:00 PM ET**. Preserve Sunday recording and submission time. Do not assume optional integrations will fit.

## 1. Scope and ownership

The core is six reviewed operating-point cards, strict provenance checks, deterministic comparison, read-only pages, CLI extraction/review/export, a small honest evaluation, deployment, and recorded evidence. `PRODUCT.md` fixes the six card IDs. `ARCHITECTURE.md` fixes the interfaces and nine comparison rules.

Severyn owns source interpretation, card approval, held-back labels, final integration, and submission. Coding agents can implement bounded tickets. They cannot approve their own semantic mappings or replace the review budget.

T1–T8, including the separate human-review ticket T1b, are core. T9–T12 are optional and deferred by default. Existing GitHub ticket text is superseded wherever it conflicts with these specifications. No ticket is complete merely because a planning document exists.

## 2. Preconditions before implementation

1. Record Severyn's project choice in issue #14. Do not present the recommendation as an accepted choice.
2. Move the working copy out of `/tmp` or establish an external backup. A temporary directory is not durable storage.
3. Confirm a funded model key and an actually available model. A pending credit request is not funding.
4. Confirm deployment access and funding. Keep secrets out of git and public logs.
5. Confirm canonical-source access and the permitted quotation/redistribution policy for the four seed sources.
6. If cloud coding agents are used, confirm their repository access. Local work must not wait for optional cloud setup.

Without a funded model key, the static core can proceed. Extraction and baseline remain explicitly `not_run`, and the complete AI-workflow acceptance remains unmet. Do not replace the missing evidence with a simulated successful run.

## 3. Twelve-hour allocation

This is a scope budget, not a measured implementation duration or a success prediction. It includes focused solo review and integration. Agents can work during the same block only after their interface prerequisites land. Their work still requires review.

| Work | Focused solo hours | Exit condition |
|---|---:|---|
| Decision and prerequisite setup | 0.50 | Choice, funding, repository safety, source access known |
| T1 schema/source anchors and interface acceptance | 1.00 | Schema and four source manifests stable before downstream work |
| T1b six-card semantic review and human labels | 1.75 | Six approved records, explicit unknowns, three dev examples approved, held-back material frozen |
| T2 strict checks and source handling integration | 1.25 | Exact spans/tokens and Litinski derivation integrated |
| T3 rule engine and verdict wording | 1.00 | Nine rule rows, correct unknown handling, dev regressions complete |
| T4 shell plus T8 first deployment | 0.75 | Logged-out shell and health route reachable |
| T5 card/compare/static-evidence pages | 1.00 | All required read-only surfaces wired to committed artefacts |
| T6 genuine extraction and local review/export | 0.75 | Actual saved run and export decisions, or explicit unmet funding prerequisite |
| T7 evaluation and baseline | 1.00 | Held-back counts, errors, uncertainty, and actual baseline status saved |
| Final integration review and live inspection | 0.75 | Main owner performs final checks and reviews public wording |
| Recording, submission copy, and submission | 1.25 | Real live-site recording ≤2 minutes and complete submission |
| Reserved repair/deployment buffer | 1.00 | Unallocated until a core problem requires it |
| **Total** | **12.00** | Includes review, deployment, recording, and buffer |

The card review budget assumes the four sources are accessible and the six-card scope remains fixed. Stop optional work if source ambiguities consume the buffer. Do not hide unresolved evidence or silently reduce the six-card acceptance.

### Calendar order

- **Friday, light setup:** choose the project and resolve prerequisites. Start T1 schema/source-manifest work only if proceeding.
- **Saturday, first block:** accept T1 schema before dependent tickets. Deploy T4 through T8 as soon as the shell exists. This first deploy does not wait for extraction or final cards.
- **Saturday, main block:** complete source/card review, strict checks, comparison, and read-only pages. Freeze the extraction prompt and human gold before held-back execution.
- **Saturday, by 17:00 ET:** aim to execute the small held-back run with the current frozen configuration. Preserve all errors. Do not start optional integrations to avoid an uncomfortable result.
- **Saturday close:** public core pages and actual run/evaluation artefacts should be available. If not, Sunday is core repair and submission only.
- **Sunday, by 13:00 ET:** freeze the demonstrated data and record against the deployed site. Allow a later replacement only if the real build improves.
- **Sunday afternoon:** finish copy, inspect logged-out routes, and submit by 20:00 ET. The deadline remainder is contingency, not planned feature time.

These checkpoints are targets. Missing one requires a truthful status decision, not fabricated outcomes or an unsupported claim of completion.

## 4. Authoritative T1–T12 ticket specifications

All implementation statuses below are **not started**. Optional statuses are **deferred**. Research and prototype work do not satisfy these product tickets. Dependencies refer to accepted interfaces or data, not merely a branch that exists.

### T1 — Schema, four pinned manifests, six draft operating points

**Status:** core / not started. **Depends on:** project choice and source access.

**Owned files:** `ledger/schema.py`, `data/sources/`, permitted `data/text/`, `data/cards/`, `tests/test_schema.py`, `tests/test_cards.py`, initial `pyproject.toml`, `uv.lock`, `Makefile`, `.gitignore`.

**Deliver:** the exact six card IDs from PRODUCT. Keep one operating point per card and layer/bound/statistic/context per metric. Separate G25's Table 5, active, and layout widths. Anchor every source-stated number to pinned canonical text. Mark seed records `research_draft` until reviewed. Review status and code-check status are independent.

**Acceptance:** the schema rejects ambiguous operating points, observed values without numeric evidence, and unknown facts encoded as known facts. Four manifests identify version/capture, licence decision, canonicalizer, and hash. Six typed seed records remain `research_draft`; T1 does not certify them. Restricted full texts remain private. No source-only discrepancy is silently corrected. Close T1 when this interface and draft data are accepted; publication review belongs to T1b after T2, avoiding a dependency cycle.

### T1b — Human review of six seed cards and development labels

**Status:** core / not started; human-owned. **Depends on:** T1 schema/drafts and T2 strict checks.

**Owned files:** reviewed `data/cards/` and source-manifest review decisions; frozen human labels supplied to T3/T7 through their stated interfaces.

**Deliver:** Severyn checks each source/operating point, numeric mapping, semantic context, unknown and licence decision. Run T2 on current hashes; only approved records become `human_reviewed`. Freeze the three development labels before T3 implementation. Prepare held-back extraction gold without exposing it to the implementation agent. Human labelling of held-back comparison pairs occurs later under T7 after the engine freezes; it is not a condition for closing T1b.

**Acceptance:** six reviewed records and three development labels with identity/time and explicit unresolved fields. No agent approves its own semantic mapping. Held-back material stays out of engine tests/prompts until the first run. The 1.75-hour review allocation above includes this ticket; it is not extra scope.

### T2 — Canonical source handling and strict provenance

**Status:** core / not started. **Depends on:** T1 schema/manifests.

**Owned files:** `ledger/sources.py`, `ledger/verify.py`, `scripts/check_cards.py`, `tests/test_sources.py`, `tests/test_verify.py`.

**Deliver:** `fetch_source`, `load_source`, and `verify_card` from ARCHITECTURE. Hash-pinned canonical text, exact span/token offsets, complete numeric grammar, explicit ambiguity failures, and the fixed Litinski k11 derivation. No fuzzy certification, digit-subsequence matching, flattened-exponent inference, or generic expression evaluator.

**Acceptance:** regression cases cover mismatched hashes/offsets, paraphrases, partial-digit matches, multiple candidate numbers, swapped table candidates, unsupported formats, missing source text, correct explicit scale/scientific notation, and derivation inputs. Token-valid wrong-field assignments remain visible as semantic review/evaluation concerns. `not_run` never becomes pass. No general failure-statistics or typo-discovery feature is required.

### T3 — Nine-rule comparison and three development examples

**Status:** core / not started. **Depends on:** T1 schema and T1b source review/development-label approval. T3 never blocks the human's earlier card review.

**Owned files:** `ledger/compare.py`, `data/eval/dev-pairs.json`, `tests/test_compare.py`.

**Deliver:** `compare(MetricRef, MetricRef, cards)` with all nine rule results and evidence. Use three dev examples specified in ARCHITECTURE. Human labels the examples before implementation. Do not invent a positive example when source evidence is insufficient.

**Acceptance:** known conflicts yield `not_comparable`. Required unknowns without conflict yield `insufficient_evidence`. Distinguish runtime constraint from outcome. Do not equate missing inclusion maps, distributions, statistics, or budgets. Do not apply arbitrary failure-budget thresholds. Ratios require fully comparable exact unbounded values. Held-back labels must not enter this ticket or its tests before the first evaluation run.

### T4 — Read-only shell and method page

**Status:** core / not started. **Depends on:** T1 schema interface.

**Owned files:** `app/main.py`, `app/templates/base.html`, `app/templates/index.html`, `app/templates/method.html`, `app/static/style.css`, `tests/test_app.py` initial routes.

**Deliver:** ledger table, method page, health route, card links, and JSON download plumbing. Show an honest incomplete-data state during the first deployment. No sample numbers masquerade as reviewed cards.

**Acceptance:** logged-out pages, labelled controls, keyboard access, escaped quotes, visible metric-layer/scope labels, explicit unknowns, and no credentials in browser content. App startup needs neither source fetching nor model credentials. T4 owns route integration when T5 adds page modules/templates.

### T5 — Card, comparison, recorded draft, and results pages

**Status:** core / not started. **Depends on:** T4 shell, T2/T3 interfaces. Final content depends on T1 reviewed data and T6/T7 artefacts.

**Owned files:** `app/templates/card.html`, `compare.html`, `draft.html`, `eval.html`, page-loading module under `app/`, and associated page tests. Coordinate route wiring with T4's owner.

**Deliver:** clickable exact evidence, per-metric context, rule table, source/check/review labels, fixed derivation display, saved extraction draft, and evaluation results. Download only permitted evidence and sanitized artefacts.

**Acceptance:** all public claims come from committed data. Missing runs say `not_run`, not success. No live extraction/review controls, manufactured rejection, or source-independent ratio. The draft page shows the actual run's outcome even if no field was rejected.

### T6 — Source-grounded extraction and local review/export

**Status:** core / not started. **Depends on:** T1 schema, T2 interfaces, funded key for a real run.

**Owned files:** `ledger/extract.py`, `ledger/review.py`, `scripts/extract_cards.py`, `scripts/review_cards.py`, `data/drafts/`, `data/runs/`, extraction/review tests.

**Deliver:** `extract(...) -> ExtractionRun` containing `list[DraftCard]`, including separate operating points. Use canonical excerpt/full-text offsets. Save exact provider output, code checks, and sanitized metadata. Local field decisions export only fully reviewed, currently checked cards.

**Acceptance:** a real configured-model run exists when funding is available. Missing fields remain unknown. The model cannot approve itself. Logs record model, hashes, tokens/latency/cost availability, and failure status. Export blocks stale hashes, missing decisions, rejected required fields, and failed provenance. Nothing persists through Render writes. No retry loop, memory, gold examples, or live endpoint is required.

### T7 — Small evaluation, honest baseline, static results

**Status:** core / not started. **Depends on:** frozen T3 engine/rules, T6 interface, human gold/held-back labels. Paid runs require funded credentials.

**Owned files:** `scripts/run_eval.py`, evaluation tests, `data/eval/results.json`, permitted post-run evaluation artefacts. `eval-private/` holds gold/labels privately until the run freeze.

**Deliver:** one extraction dev excerpt, two held-back excerpts targeting about 12–20 numeric fields, three comparison dev examples, and three independently human-labelled held-back pairs. Freeze all hashes before the held-back run. Use stable operating-point/metric alignment, not list order. Provide a same-source-access structured LLM baseline when funded.

**Acceptance:** results contain actual counts, denominators, field-mapping errors, omissions/extras, false accepts/rejects, accepted-field errors, per-rule disagreements, descriptive 95% Wilson intervals, and exposure/uncertainty notes. Development regressions are not held-back accuracy. A second attempt is labelled a rerun. Missing funding gives `not_run`, never a fake result or a knowledge-cutoff strawman. Three pairs do not support a strong benchmark claim.

### T8 — Early deployment, reproducibility instructions, and submission integration

**Status:** core / not started. **Depends on:** T4 for first deploy. Final integration depends on T1–T7 acceptance and human submission work.

**Owned files:** `render.yaml`, `README.md`, final Makefile wiring through the integration owner, deployment settings, and submission links. Presentation documents retain their designated owner.

**Deliver:** deploy the shell early, then redeploy reviewed artefacts. Document setup, offline checks, source licence/cache restrictions, model funding, and excluded features. Record the actual live-site video and completed submission through the human owner.

**Acceptance:** live read-only routes work logged-out, the app needs no model key at runtime, data survives by git redeploy rather than local disk, the recording matches the site, and public results match saved artefacts. The main integration owner runs final checks once after edits land. No unmeasured availability, speed, or scientific-validity guarantee appears.

### T9 — Headline parser

**Status:** optional / deferred. **Depends on:** T3, T5, stable funded extraction.

**Files if enabled:** `ledger/headline.py`, separate headline template/tests, route wiring through T4 owner.

**Acceptance if enabled:** source-grounded structured assertion, explicit user confirmation of card mapping, unknown-match abstention, and normal comparison rules. No free-form headline verdict overrides evidence. It is not part of the recording's required path.

### T10 — Authentication

**Status:** optional / deferred. **Depends on:** a real restricted workflow and a durable approval design approved separately.

**Files if enabled:** isolated auth configuration/module/tests, coordinated routes.

**Acceptance if enabled:** authentication protects an actual operation. Approvals still export locally or enter durable versioned storage. Clerk sign-in plus ephemeral filesystem writes must not be presented as persistent review. Do not add a live writable reviewer during the core build.

### T11 — Memory

**Status:** optional / deferred. **Depends on:** T6 and an explicit post-core use case.

**Files if enabled:** isolated memory module/tests and configuration.

**Acceptance if enabled:** traceable retrieval, explicit unknowns, documented storage/deletion, and memory disabled in held-back evaluation. No current-best ranking across unlike classes. No SDK/pre-release integration enters the core critical path.

### T12 — Automated CI

**Status:** optional / deferred. **Depends on:** stable T2/T3 checks and source availability policy.

**Files if enabled:** workflow configuration only, with necessary integration-owner changes.

**Acceptance if enabled:** deterministic offline tests run without secrets. Redistributable pinned sources are available. Missing restricted texts produce a separate availability report, not a fabricated pass or automatic content drift. CI must not run paid model evaluations or claim universal source verification. Local check commands remain core even when CI is absent.

## 5. Dependency map and integration discipline

```text
choice/access -> T1 schema/manifests
  T1 drafts -> T2 sources/checks -> T1b reviewed cards/dev labels
  T1 schema -> T4 shell -> T8 early deploy
  T1b approved dev labels -> T3 engine
  T2 + T3 + T4 -> T5 read-only pages
  T1 + T2 + funded key -> T6 extraction/review export
  frozen T3 + T6 + human-held labels -> T7 results
  T1–T7 + T8 redeploy -> final review -> recording -> submission
```

Freeze interfaces before simultaneous edits. Give each shared file one integration owner. All tickets skip mid-flight builds, tests, linters, and formatters while shared edits continue. The main integration owner performs the final verification after all accepted changes land.

Main owner should run the implemented `make test`, `make verify`, and logged-out route checks. Model runs are intentional evaluation work, not an automatic verification prerequisite on every change. Record only checks actually exercised.

## 6. Cut policy and completion

T9–T12 start deferred and stay deferred unless core work and buffers are complete. No optional auth, memory, headline parser, or CI sophistication is required for the demo. Live extraction in the recording is not core. Recorded genuine evidence is core.

Do not silently remove the physical record, reduce six cards, replace held-back labels with memorized tests, or claim an unavailable funded model run. If a core prerequisite fails, finish reachable work and state the exact unmet acceptance. A reduced deliverable needs Severyn's explicit approval.

Completion requires:

- Six human-reviewed operating-point cards with current provenance checks and permitted evidence.
- Nine-rule deterministic comparison with abstention and no misleading ratios.
- Required logged-out card/compare/method/recorded-draft/results surfaces.
- Genuine CLI extraction and review/export evidence, or an explicit statement that full completion is blocked by unavailable funding.
- Three dev examples and three independently human-labelled held-back pairs, with separate results.
- Small extraction results, mistakes, denominators, uncertainty, and actual baseline status.
- Early deployed URL updated with final artefacts, reproducibility/limitations instructions, truthful ≤2-minute recording, and submission.

No benchmark win, semantic-proof claim, cost estimate, or success probability is prewritten as a result.

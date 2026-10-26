# QRef: build specification

Status: **review package, not an implemented product**. The user selected the bounded quantum-code migration reviewer, delegated stack selection and allowed no new paid services. This document defines the proposed complete release. Another AI should review it with [REVIEW.md](REVIEW.md) before implementation begins.

Product purpose is in [PRODUCT.md](PRODUCT.md); vocabulary is in [CONTEXT.md](CONTEXT.md). [PLAN.md](PLAN.md) defines build order and acceptance gates. The [report brief](docs/design/report-brief.md) specifies the proposed visual surface. This specification is authoritative for interfaces and behavior; archived proposals are not.

## 1. The decision

Build a **local AI-assisted migration and review tool with a portable web report**. A developer generates a proposed Qiskit port, inspects it, executes the reference and target in isolated environments, reviews independent observations and shares the resulting report.

The public site is a copy of a recorded report. It is not a hosted execution service. No account, API key, database, upload form or paid server is needed.

The first supported job is QAOA helper migration between the pinned Qiskit/Aer environments below. The tool does not revive arbitrary notebooks, reproduce an entire paper, certify science, discover better circuits or prove whole-program equivalence.

### Why this is useful enough to build

A circuit can be equivalent while the surrounding experiment changes. The real seed migration demonstrates this: circuit checks agree, but the target honors requested shots that the reference ignores. That can be a correction, not an error. A reviewer needs the observations, the model's stated intent and a separate human disposition.

Qiskit, Aer and MQT QCEC already provide the underlying capabilities. The contribution is a reproducible review protocol and readable evidence—not a new equivalence engine. A normal coding agent plus ordinary tests is a strong substitute. No adopting user, time saving, moat, revenue or probability of winning is established.

## 2. Complete release and exclusions

### Required outcome

A fresh supported local run must produce:

1. Copied, content-identified reference and target inputs.
2. Actual execution observations from both pinned environments.
3. Checks of submitted circuits, declared classical interpretation and shot settings.
4. A versioned immutable evidence record, complete coverage inventory and explicit limitations.
5. A self-contained HTML report, exact evidence JSON and portable export bundle.
6. A hash-bound human decision input and a way to regenerate the report with that decision.
7. A free public copy of a real report, plus reproducible local commands.

The curated release must come from a fresh successful **implemented `qref propose`** invocation, inspected before execution. Its resulting bound case, proposal artifacts and export are committed for an explicitly labelled recorded demo. The old research receipts are capability evidence, not production-format proposal records to invent or silently convert. Offline replay uses that future curated case; no fake live model call or progress is allowed.

### Deliberate exclusions

No arbitrary public Python execution, web uploads, notebook discovery, hardware, cloud quantum credentials, noise, dynamic circuits, optimizer convergence, multi-user collaboration, account system, review database, provider abstraction, automatic repair loop, discovery arena, threat estimator, automatic scientific approval or sponsor-only integration.

No theme switcher, circuit animation, graph editor, command palette, report history, custom PDF engine or separate marketing landing page. These are outside this release, not unfinished promised features.

## 3. What exists and what has been proved

| Material | Observed result | Limit |
|---|---|---|
| [Seed evidence](evidence/qaoa/README.md) | Source, real Sonnet port, notes, exact dependency lists, 18 observations per runtime and nine circuit comparisons are retained. | The old observer rebuilt a circuit separately from the sampled execution and omitted several provenance fields. It is research code, not the product observer. |
| Fresh proposal capability probe | Claude Code 2.1.308, existing claude.ai Pro login, tools disabled and structured output produced a complete target module and notes. No API key was needed. | One CLI invocation, not a model-performance benchmark or billing proof. The prompt supplied the known shot behavior and requested its correction/disclosure. |
| Fresh capture capability probe | A scoped `AerBackend.run` hook captured the actual submitted circuits in both runtimes. Each produced 18 observations. Independent classical checks covered 64 basis assignments per side. | Positive feasibility only. Failure handling, complete schemas, packaging and all unsupported branches remain to be implemented. |
| Captured-circuit comparison | Nine distinct submitted circuit pairs were equivalent; all 18 execution pairs were covered. Requested/completed shots still differed as expected. | One inspected port and finite inputs. The fresh model followed an explicit shot-correction instruction; it did not independently discover that issue. |
| Deployment prerequisites | The repository is public; Pages was not enabled when checked. Official Pages workflows support the chosen static output. | No QRef site or deployment workflow exists yet. |

Fresh probe source/results are captured on branch `research/qref-spec-probes`; [planning verification](docs/reviews/planning-verification.md) records the immutable publication pointer and exact scope. Original probe revision is `825140ea1394941fd006752a57dcaa96b182ed0e`. Do not invent timestamps, code bindings or environment metadata for older observations that did not record them.

The old planted-error prototype and competing project research are under [the archive](archive/research-2026-10/README.md). They are not the production implementation or an observed agent-error rate.

## 4. Chosen stack and deployment shape

| Concern | Decision | Reason |
|---|---|---|
| Runtime | CPython 3.11.12; installable `src/qref` package; `uv` lock/setup | Matches exercised scientific environments and keeps one toolchain. |
| CLI | Standard-library `argparse`; `qref` console entry point and `python -m qref` equivalent | No daemon or CLI framework required. |
| Contracts | Packaged JSON Schema Draft 7 plus explicit semantic validation | Same dialect works with Claude structured output; cross-record invariants still need code. |
| Validation | `jsonschema==4.25.1` | Mature structural validation; avoid a second competing model hierarchy. |
| Rendering | `Jinja2==3.1.6`, explicit HTML autoescaping, `StrictUndefined` | Safer than hand-interpolating source/log text into HTML. |
| Interaction | Packaged CSS and small vanilla JavaScript, embedded in the HTML | Offline report and no Node build. Essential facts render without JavaScript. |
| Scientific execution | Pinned Qiskit/Aer environments; MQT QCEC in the target environment | Reuse established engines. Keep incompatible NumPy namespaces apart. |
| Hosting | GitHub Pages, official GitHub Actions artifact deployment | Public open-source report, no paid host or server. |
| Tests | Existing project gains focused pytest behavior tests during implementation; actual browser/CLI smoke remains mandatory | Tests cover consumer-visible failures, not source wording or copied configuration. |

Keep scientific libraries in a `quantum` optional dependency group. Base rendering/validation must work without importing Qiskit, Aer, NumPy or QCEC. Pages CI installs base dependencies only and renders already recorded evidence. It never runs a candidate or calls a model.

The implementer must create the actual project metadata and `uv.lock`, resolve build-backend dependencies, and verify package data inclusion. No fake lock or executable acceptance command is claimed by this plan.

### Scientific pins

| Package | Reference | Target/checker |
|---|---|---|
| Python | 3.11.12 | 3.11.12 |
| Qiskit | 0.46.3 | 2.6.1 |
| Aer | 0.14.2 | 0.18.0 |
| NumPy | 1.26.4 | 2.4.6 |
| NetworkX | 2.8.8 | 2.8.8 |
| SciPy | 1.17.1 | 1.17.1 |
| MQT QCEC | Not installed/required | 3.11.0 |

Use the full [reference](evidence/qaoa/legacy-requirements.txt) and [target](evidence/qaoa/modern-requirements.txt) snapshots to bootstrap. Qiskit 2.6.1 requires NumPy 2; a shared NumPy 1.26.4 environment is invalid. Fresh Linux scientific installation is not proved by the macOS runs. The public render job does not require that installation.

## 5. End-to-end workflow and exact CLI

The commands below are **proposed interfaces**. They do not exist until implementation passes its gates.

### Setup

The implementation README must give exact fresh-clone commands. Target shape:

```bash
uv sync --frozen --extra quantum
uv venv --python 3.11.12 .qref/envs/reference
uv pip install --python .qref/envs/reference/bin/python -r evidence/qaoa/legacy-requirements.txt
```

The target interpreter is `.venv/bin/python`. The reference interpreter is `.qref/envs/reference/bin/python`. A run does not install, update or repair its environments. It checks actual versions first. No fallback to whichever Python happens to be on PATH.

### Generate a proposed port

```bash
uv run qref propose --case cases/qaoa.json --out runs/proposal-001
```

This reads the declared reference, target-version constraints and fixed migration instructions. It invokes the authenticated local Claude CLI once, without a shell, using piped input. It writes a proposed `target.py`, notes, a proposal record, copied reference/pins and a new portable `case.json` pointing at those files. **It never imports or executes the target.** The user inspects the generated source before the next step.

The normal route uses the existing subscription, not pending API credits. Resolve one Claude executable and record `claude --version`; the exercised supported release is 2.1.308. A different release requires a deliberate compatibility check, not an automatic update. Before any model request, run `[executable, "auth", "status"]` from the temporary cwd with a 15-second deadline. Require exit 0, valid JSON, `loggedIn is true`, `authMethod == "claude.ai"` and `apiProvider == "firstParty"`. Discard account identity; retain only these categories.

Use the **same effective child environment** for status and generation. Reject nonempty variables matching `ANTHROPIC_*` or `CLAUDE_CODE_USE_*`, and the exact names `CLAUDE_CODE_OAUTH_TOKEN` and `CLAUDE_CONFIG_DIR`, rather than silently selecting a different billing route; log names, never values. Construct the child environment from `HOME`, `PATH`, `TMPDIR`, `LANG`, `LC_ALL`, `LC_CTYPE`, `TERM`, `USER` and `LOGNAME` only. All other environment values are excluded. The fixed setting-source restrictions exclude user/project helpers; managed-policy isolation is not attested. Status failure or an unrecognized category means no model request. Do not extract tokens, purchase credits, switch providers, update Claude, or silently replay output. This is a conservative spending guard, not proof of billing.

The exercised invocation uses `--restricted -p`, `--model sonnet`, `--effort high`, `--tools ""`, an empty strict MCP configuration, requested disabling of hooks/auto-memory/connectors/synced plugins and skills, `--disable-slash-commands`, `--no-session-persistence`, `--setting-sources ""`, JSON output and `--json-schema`. See [verification](docs/reviews/planning-verification.md) for the exact tested argv. Run from a fresh temporary directory, not the candidate repository. Use a 180-second outer generation deadline, terminate/reap the process group on expiry and never retry automatically. These controls are not an OS sandbox or a guarantee about overriding managed policy.

**Do not use `--bare`: official docs say it does not read subscription OAuth/keychain credentials and requires API/provider authentication.** That conflicts with the selected subscription-only path.

Accept only process success, a successful non-error CLI result, a present `structured_output`, valid schema and syntactically valid Python. Do not parse code from free-form `result` as a fallback. A refusal, missing structured output or invalid code leaves an error record, not a successful proposal.

Proposal output has exactly `code: string`, `summary: string`, `intentional_changes: string[]`, `uncertainties: string[]`. The source is prompt data, not executable instructions. Record exact prompt/schema/source/output hashes, timestamps, CLI version, resolved model, usage and the CLI cost estimate. Label that estimate as an estimate, not an invoice. One CLI invocation may contain internal SDK turns; do not claim one invocation equals one API request.

Proposal failure uses a separate `qref.proposal-error/v1` record: `schema`, `state` (`incomplete|failed`), `stage` (`initialization|auth|cli|response|syntax|write`), `reason_code`, bounded sanitized `message`, actual `started_at`, nullable `finished_at`, nullable `cli_exit`, and `artifact_refs`. Codes are `proposal_incomplete`, `auth_unavailable`, `auth_category_rejected`, `billing_override`, `unsupported_cli`, `cli_timeout`, `cli_failed`, `response_invalid`, `syntax_invalid`, `write_failed`. Do not fabricate successful output/hash fields.

Validate inputs and exclusive output-directory creation first; a failure before that writes no promised directory. Then atomically write an incomplete `proposal-error.json` checkpoint before starting work. On a caught failure, finalize that record and retain only copied inputs and bounded private diagnostics; no `case.json` or successful proposal record. On success, write validated target bytes and all supporting artifacts, publish `proposal.json`, remove the error checkpoint, and atomically publish portable `case.json` **last**, as the runnable commit marker. A hard interruption may leave partial files but must not leave a runnable case. `run` rejects a case whose bound proposal directory still has an error checkpoint. Proposal code bytes are exactly UTF-8 encoding of `output.code`, with no automatic newline or formatting change.

### Execute and review machine evidence

```bash
uv run qref run --case runs/proposal-001/case.json \
  --reference-python .qref/envs/reference/bin/python \
  --target-python .venv/bin/python \
  --out runs/run-001 --trust-local-code
```

Before a curated production case exists, `cases/qaoa.json` may run the inspected legacy research port with `proposal=null`; its research provenance remains visible, but it carries no invented `qref.proposal/v1` attribution. Release integration must instead use the fresh Gate C proposal, then preserve that exact case for later recorded replay.

`--trust-local-code` is required before any candidate import. Its help text states that Python can access local files, network and process credentials. Virtual environments and subprocesses isolate versions, **not hostile code**. Only inspected code belongs in this workflow.

A completed run writes the evidence and a first report even when differences require review. Its exit code is not a scientific certificate. Never chain report publication to an assumed all-green result.

### Record a human decision and re-export

The immutable run contains a valid pending `review-template.json`. Copy it outside that run before editing:

```bash
cp runs/run-001/review-template.json runs/review-001.json
```

Fill the actual reviewer, decision and rationale. Then:

```bash
uv run qref report --run runs/run-001 --decisions runs/review-001.json \
  --out exports/run-001-reviewed
uv run qref verify-bundle --run exports/run-001-reviewed
```

`report` validates the original bundle, validates the overlay, then writes a **new** export. It does not execute Python or a model. Editing the immutable run or its template in place is not the review workflow. The browser displays recorded decisions; it does not pretend to save approval.

All output directories must be new. No overwrite, resume, automatic retry or migration-repair loop in this release.

## 6. Supported case contract

`cases/qaoa.json` uses `schema="qref.qaoa-case/v1"`. Paths resolve relative to the case file. Snapshot input bytes before execution; workers read snapshots, not mutable original files.

| Field | Required meaning |
|---|---|
| `schema`, `case_id`, `title`, `description` | Version plus plain descriptive identity. IDs match `[a-z][a-z0-9_-]*` and cannot contain `/`. Display names are not content identity. |
| `origin` | `real_migration`, `positive_control` or `seeded_regression`. Synthetic regressions must never appear as naturally observed agent errors. |
| `reference`, `target` | Each has `module`, `pins` and `receipt`. File paths are relative to the case. One helper file per side; no supporting local module discovery. |
| `graphs` | Unique IDs; node list exactly `0..n-1`; explicit ordered edges; simple undirected unweighted graph; no loops or duplicate/reversed duplicate edges. First supported range: 1–8 qubits. |
| `angles` | Unique IDs and nonempty finite even-length `theta`; first half beta, second half gamma, radians. First supported depth: one or two layers. |
| `shots` | Ordered unique positive integers, not booleans or coerced strings. |
| `interpretation` | `negative_maxcut`, `node_i_is_qubit_i`, `qiskit_count_msb_left`, terminal identity measurement map. |
| `proposal` | Null, or paths to the bound proposal record, prompt/response/notes. Mode is `recorded` or `new_local_call`. No attribution to a model when no record exists. |

Each side's `receipt` has exactly `kind` (`upstream_extract|local_code|model_port`), nullable `upstream_url`, `upstream_revision`, `upstream_path`, nonempty `extraction_scope` and `attribution`, `license_spdx`, relative `license_file`, and nullable `derived_from_sha256`. Upstream extracts require all three upstream fields; URLs are HTTPS without userinfo, otherwise displayed only as text. Model ports bind the reference module digest and retain its applicable licence/attribution; do not invent an upstream author. Copy and hash the full licence text. Local cases can declare `NOASSERTION`, but such a run is not eligible for the curated public export without an explicit rights review.

The seed receipt identifies Qiskit textbook revision `0ae905083ec3872d7ddc6bb4001d5468f476d93f`, `content/ch-applications/qaoa.ipynb`, helper cell 18 plus declared imports, the Qiskit textbook contributors and Apache-2.0. The bundled full reference source means the extracted helper module, not a claim to have executed the whole notebook.

Limit a case to at most 64 executions per side. This is a local resource bound, not a security claim. Broader inputs within these proposed limits need implementation acceptance tests; present feasibility covers the seed's four- and five-qubit inputs only.

Supported helper functions are `maxcut_obj(x,G)`, `compute_expectation(counts,G)`, `create_qaoa_circ(G,theta)` and `get_expectation(G,shots=512)`, returning a callable of theta. The module's returned scalar must represent the observed counts under the declared interpretation.

The seed uses:

- `textbook_cycle4`: edges `[[0,1],[1,2],[2,3],[3,0]]`.
- `asymmetric4`: edges `[[0,1],[1,2],[2,3],[0,2]]`.
- `cycle5`: edges `[[0,1],[1,2],[2,3],[3,4],[4,0]]`.
- Angles `[0.17,0.63]`, `[0.81,0.29]`, `[0.17,0.63,0.41,0.92]`.
- Shot requests `[512,17]`.

The full Cartesian product gives 18 executions per side and nine graph/angle cases. Execution IDs are `graph_id/angle_id/shots-N`. Define `canonical(x)` as Python JSON with sorted object keys, compact separators `(",",":")`, UTF-8, `ensure_ascii=False`, `allow_nan=False`, no BOM or final newline; preserve array order and parsed numeric values without coercion. `input_sha256` hashes canonical `{"graph":{"nodes":nodes,"edges":edges},"theta":theta,"requested_shots":N,"interpretation":interpretation}`. Shot count belongs here. IDs alone never establish pairing.

Construct NetworkX graphs by adding the declared nodes first, then the ordered edges. Constructing only from edges would silently drop isolated nodes and break valid one-qubit or disconnected inputs.

Reject unknown schema versions, duplicate JSON keys, non-finite numbers, ambiguous IDs and invalid dimensions before execution. Use packaged schemas only; no remote schema resolution. Cross-file hashes, timestamps, inventory and domain invariants require explicit validation beyond JSON Schema. `format` annotations alone do not validate dates.

If proposal attribution is present, its reference and generated-code digests must match the snapshots. A manually edited target must not retain exact-output attribution. Supply an explicitly manual case without that claim, or regenerate a proposal. Do not silently rebind stale model notes.

### Exact identity scopes

- A file SHA-256 hashes exact file bytes, never its path or a reserialized representation.
- `case_sha256` hashes the unchanged original case bytes copied to `artifacts/inputs/case.original.json`. Workers receive explicit snapshot paths; they must not resolve that original case's paths back into mutable originals.
- Write a portable root `case.json` with paths to the copied module/pin/licence/proposal artifacts. Evidence binds both its bytes and the original case bytes. Replaying it creates a new run/identity, not an identical historical timestamp.
- `checker_config_sha256` hashes canonical `{entrypoint,kwargs,importer_policy,global_phase_policy,checker_version,qiskit_version,effective_defaults,unknown_reasons}`. The entrypoint is `mqt.qcec.verify`; actual kwargs/default-call provenance and versions are recorded. Unknown exposed defaults are null with reasons, not guessed.
- `circuit_result_id` is `circuit-result-` plus SHA-256 of canonical `{reference_qasm_sha256,target_qasm_sha256,checker_config_sha256}`. These are the exact measurement-free engine inputs. **Exclude shots, execution IDs, graph/angle labels and QPY bytes.** List all covered execution IDs; same engine inputs can cover both shot requests.
- Actual measured QPY, metadata and analysis-QASM files each retain their own byte digest. Global phase is retained in the measured record but deliberately ignored by the circuit comparison policy; QASM2 is not called a lossless circuit snapshot.
- The displayed run identity is the full exact-byte `evidence_sha256`; a shortened display must expose the complete value. There is no second invented run ID.

## 7. Execution design

### Process and file rules

Run reference and target serially in their supplied interpreters, with an explicit accessible working directory owned by the run, never an inherited protected/source cwd. Invoke the trusted standalone worker file by absolute path, with an argv list and `-I`; do not use shell interpolation. The worker must not import the installed QRef package, Jinja or schema libraries, because the reference environment intentionally lacks the target dependency set.

Check actual Python and required distribution versions before candidate import. Record complete distribution inventories and OS/architecture. Normalize package names for comparison; additional installer/tool distributions may be recorded, not silently mistaken for a pin mismatch. Absolute interpreter/home paths belong in private diagnostics, not public identity fields.

Use one outer 120-second deadline per observation worker, 30 seconds per QCEC worker and a 120-second total circuit-check budget. Terminate and reap expired process groups. No retry or fallback. These controls manage inspected code; they do not contain malicious descendants or establish hard real-time guarantees. Preserve useful completed diagnostics when a stage fails.

Candidate stdout/stderr goes to separate bounded diagnostic logs, not the JSON protocol. Record truncation. Workers atomically replace their observation document after each execution, so a killed worker does not leave a half-parsed JSON result. Never fill missing observations with zero values.

### Capture actual submissions

Install a scoped `AerBackend.run` class hook before candidate import and restore it in `finally`. Reject backend execution during import or outside an active declared execution. The hook forwards all original positional/keyword arguments unchanged and captures the circuit **before** submission. Do not rely on a closure variable named `backend`.

For each objective invocation require exactly one backend run, one submitted circuit and one result experiment. Accept a single circuit or a one-element sequence. More or fewer executions are unsupported, not a fabricated empty pass. A renamed closure variable must not break supported capture.

Retain actual measured circuit identity, qubit/classical dimensions, terminal measurement map, layout metadata, backend class/options, run kwargs, result status, completed shots, raw counts and returned scalar. Before forwarding the backend call, copy the actual circuit and write it with that side's `qiskit.qpy.dump` to a measured `.qpy` artifact. Record producer Qiskit version and a JSON metadata artifact containing ordered register names/widths, flat-wire indices, raw measurement map, layout and finite global phase. QPY is a retained opaque native snapshot; the renderer/verifier never loads it, and the other runtime need not load it.

Supported circuit shape is a static unitary followed by one terminal identity measurement per qubit, one classical register of width n and no nonidentity layout. Reset, control flow, mid-circuit measurement, noise, unbound parameters, multiple classical registers, ancillas, changed/non-bijective maps or nonidentity layouts are **unsupported** in this release. Preserve the raw map and reason. Do not remove operations to make a case look supported.

After shape validation, remove only terminal measurements from the captured copy for analysis. Export bounded QASM2 from that actual submission. QASM2 is the explicitly lossy checker input; measured QPY/metadata retain phase/register/layout information. Use the exercised `qasm2.loads(..., custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS)` path for legacy `rzz`. Do not introduce a new parser, external includes or unexercised QCEC methods. QPY capture itself remains an implementation acceptance requirement, not a claim about the earlier probe.

### Independent interpretation

The worker records raw counts, module-returned objective, that module's weighting of captured counts, exact probabilities from the submitted circuit, module weighting of those probabilities and direct classical basis-table outputs. The parent performs independent interpretation from those recorded values.

The independent negative-cut rule is:

```python
-sum(((k >> u) & 1) != ((k >> v) & 1) for u, v in edges)
```

This rule must not call either program's helper. It is a declared case interpretation, not a universal science oracle. Enumerate all n-bit assignments once per graph and side to check sign/indexing and the count-string decoder. Test weighted histograms too; a basis table alone does not establish arbitrary aggregation correctness.

Qiskit count strings put bit zero on the right. Retain this convention and the actual measurement map. Compare each returned sampled scalar with independent decoding of **its own captured counts**. Do not compare noisy sampled means or count histograms for exact equality between runtimes. Seed 10 does not establish matching random streams across simulator versions.

Compute full ideal distributions over the declared all-zero initial state and bound angles. Use absolute tolerance `1e-10`, relative tolerance zero, for QRef's finite numerical comparisons. Record it. This is separate from QCEC's engine configuration. Finite numerical agreement is not proof for all inputs.

## 8. Checks, outcomes and complete coverage

The normalized check status enum is exactly `pass | difference | inconclusive | unsupported | error`. Every required check has a record, including blocked checks.

| Check | Criterion |
|---|---|
| Pairing | Unique expected execution IDs, exact input digests, both sides and complete coverage inventory. Reordering records cannot change the result. |
| Submitted circuits | Definitive QCEC equivalence under fixed-wire/global-phase policy. |
| Measurement interpretation | Declared identity map and supported dimensions/layout. Unsupported maps block dependent interpretation. |
| Ideal probabilities | Maximum absolute difference across all declared outcomes ≤ tolerance. |
| Exact objective | Independent negative-cut expectations agree within tolerance. |
| Classical basis behavior | Both module helpers agree with the independent rule on every basis assignment. |
| Classical weighting | Module expectation agrees with independent weighting of captured counts and exact probabilities. |
| Returned result | Returned scalar agrees with independent decoding of the same captured histogram. |
| Shot integrity | Completed shots equal count sum; a mismatch is `error/invalid_sampling`, invalid result evidence, never an intentional policy difference. |
| Shot request | Per-side completed shots equal requested shots. The reference may violate this. |
| Shot preservation | Reference and target completed shots agree. This is separate from honoring the request. |

Capture every requested-shot execution before deduplicating. Cache only identical reference-QASM, target-QASM and engine-configuration digests **within this run**. No persistent cache. Each unique circuit result lists the execution IDs it covers.

Expected check IDs must remain constructible when a worker fails. Therefore keep one logical `circuit/<execution_id>` check slot per expected execution, referring to a deduplicated `circuit_result_id` when available. Missing prerequisites create an inconclusive slot with a reason; do not require a nonexistent QASM hash to name a blocked check. The headline count of distinct circuit pairs comes from actual results, not a hardcoded nine.

Other stable check IDs are `measurement/E`, `probability/E`, `exact-objective/E`, `classical-basis/S/G`, `classical-weighting/S/E/counts`, `classical-weighting/S/E/exact`, `returned-objective/S/E`, `shots-integrity/S/E`, `shots-request/S/E` and `shots-preservation/E`, where E is execution ID, S is `reference|target`, G is graph ID. The global pairing check is `pairing`.

### Prerequisite and failure matrix

Apply these rules before a check's ordinary numerical/semantic criterion. Valid supported comparisons pass on equality/tolerance and differ on a genuine mismatch; no other state becomes a difference by default.

| Condition | Check outcome | Dependent checks / run effect |
|---|---|---|
| Duplicate/unknown ID, wrong input/content binding, malformed observation | `error` with `duplicate_or_unknown_id`, `input_binding_mismatch` or `invalid_observation` | Pairing error; invalid run. Preserve raw diagnostics, not trusted comparison values. |
| Completed-shot/count-sum mismatch or invalid sampling payload | `shots-integrity/S/E = error`, `invalid_sampling` | Invalid run; dependent numeric/request/preservation checks are inconclusive. Never create an accept-intent finding from it. |
| Missing prerequisites, `not_run` or `incomplete` checkpoint | `inconclusive`, `missing_prerequisite`, `not_run` or `worker_interrupted` | Missing completed coverage; retain any independent valid checks. |
| Worker/import/environment failure | Affected checks `inconclusive`, `worker_failed`, `import_failed`, `worker_timeout` or `environment_mismatch` | Failed/partial precedence below; log the actual failure separately. |
| Unsupported shape/map/layout/run cardinality/option | `unsupported` with `unsupported_circuit`, `unsupported_measurement`, `unsupported_layout`, `unsupported_backend_execution`, `import_time_execution` or `unsupported_option` | Dependent checks unsupported, not interpreted under a guessed representation. |
| Unexpected checker/infrastructure exception or worker resource cap | `error`, `checker_exception`, `infrastructure_error` or `resource_limit` | Apply ordered failed/partial precedence; known differences remain visible. |
| Ordinary valid finite mismatch | `difference`, `numeric_mismatch`, `classical_rule_mismatch`, `shots_request_mismatch`, `shots_preservation_mismatch` or `circuit_not_equivalent` | A reviewable finding; no invalidity inferred merely from a behavior change. |

Successful checks use `reason_code="equal"`. QCEC inconclusive codes are `timeout`, `checker_budget_exhausted`, `checker_no_information`, `checker_probable` and `checker_unknown`. These and the matrix codes form the closed check-reason vocabulary for v1; exception text belongs in bounded logs. Execution states map as follows: `completed` permits ordinary checks; `failed` blocks dependent checks as inconclusive; `unsupported` blocks them as unsupported; `incomplete|not_run` blocks them as inconclusive. A completed pair requires **both records to have `state=completed`**, not merely initialized entries.

### QCEC mapping

Preserve the raw criterion, actual package version/configuration and checker result artifact. Compare exact enum names, not truthiness or substring matches.

| Criterion | Normalized result |
|---|---|
| `equivalent` | pass; exercised in the positive probe |
| `equivalent_up_to_global_phase` | pass under declared global-phase policy; a fresh global-minus-one gate probe exercised this value |
| `not_equivalent` | difference; the fresh relative-Z probe exercised this value |
| `equivalent_up_to_phase` | inconclusive; do not broaden the global-phase policy |
| `probably_equivalent`, `probably_not_equivalent`, `no_information` or an unknown future value | inconclusive; retain the raw value |
| Outer deadline | inconclusive, `timeout` or `checker_budget_exhausted` |
| Unsupported representation/shape | unsupported, with the affected scope |
| Unexpected checker exception | error, with type and log artifact |

Use the exercised `qcec.verify` entrypoint. Living docs describe newer method/timeout features; do not assume they exist in the installed pin. Parent subprocess deadlines are sufficient here.

**Binding-docstring trap:** v3.11.0's Python registration descriptions reverse the two phase explanations. Do not swap this table based on those docstrings. The pinned alternating-checker source explicitly returns `EquivalentUpToGlobalPhase` when the identity has a non-one global weight; the runtime probe returns that enum for a gate-level global minus sign and `not_equivalent` for a relative-Z change. Preserve this counter-evidence in acceptance. Metadata-only Qiskit global phase was ignored by the tested import path, consistent with this policy; it is not evidence that QASM2 preserves phase.

### Aggregation

`run_state` is `complete`, `partial`, `failed` or `invalid`:

Apply this ordered procedure; first matching rule wins:

1. **Invalid:** case/content binding, observation structure, pairing or sampling integrity is invalid. A schema-valid diagnostic evidence record is allowed, but no scientific comparison is presented as valid.
2. **Failed:** zero expected pairs completed and a worker or execution failed. An unsupported-only run is not called execution failure.
3. **Partial:** any expected pair is not completed, or an unexpected infrastructure/checker error occurred.
4. **Complete:** every expected pair has both sides completed and no preceding rule applies. A checker may still be inconclusive/unsupported.

`evidence_summary` is `incomplete` if run state is not complete or any required check is inconclusive/unsupported/error; otherwise `difference` if any check differs, else `consistent`. This precedence is unconditional. Known differences remain visible alongside incomplete status.

Only valid `difference` checks create human-review findings. Group shot **request and preservation** differences into one `shot_policy` finding; shot integrity errors stay separate diagnostic checks and cannot be accepted as intentional. Other finding IDs are their check-kind names, one group per kind. Bind decisions to the exact evidence digest and finding ID. Repeated observations are not independent bugs.

| Run/evidence state, in precedence order | Main report state | `run` exit |
|---|---|---|
| `invalid` | `Invalid observations — comparison unavailable` | 2 |
| `failed` | `Execution failed — comparison unavailable` | 2 |
| `partial` or summary `incomplete` | `Comparison incomplete`, plus known differences | 2 |
| `complete` / `difference` | Evidence-derived change headline; differences need review | 1 |
| `complete` / `consistent` | `No differences on declared inputs` | 0 |

### Exit codes

| Command | Meaning |
|---|---|
| `propose` | 0: valid proposal artifacts; 2: authentication, CLI, schema, syntax, input or write failure |
| `run` | 0: complete consistent bounded evidence; 1: complete evidence with differences; 2: incomplete/invalid/unsupported/error or command failure |
| `report` | 0: valid export written, even if its evidence contains differences; 2: invalid evidence/overlay/integrity or write failure |
| `verify-bundle` | 0: declared bytes and record links are consistent; 2: validation failure |

Human decisions never alter `run` exit semantics. Exit 0 never means whole-program or scientific correctness. Before valid setup, input/output-directory errors return 2 and promise no report. After valid snapshots, all four run states emit a schema-valid diagnostic/comparison evidence record, coverage slots, bounded available artifacts, pending template and appropriately labelled report. If the host cannot safely write those files, return 2 and report that write failure; do not reuse an earlier run. A structurally invalid **bundle** is refused by `report`/`verify-bundle`; a well-formed diagnostic record whose `run_state=invalid` may render a diagnostic page, never a normal comparison.

## 9. Evidence and review records

Use one packaged `protocol.schema.json` with local definitions for case, successful proposal output/record, proposal error, observations, evidence, decisions and manifest. Freeze these shapes in the first implementation gate. Reject unknown fields/version drift rather than guessing. Do not duplicate the contract in a second runtime model hierarchy.

### Evidence record: `qref.evidence/v1`

| Required field | Contents |
|---|---|
| `schema` | Exact version string. |
| `case` | `{definition,case_sha256,source_artifact,portable_case_artifact,portable_case_sha256}`; validated original definition plus exact original/portable case-file bindings. |
| `provenance` | Actual execution times, environments, QRef version when known, observer/comparison hashes, input/pin hashes, both bound source receipts, proposal references and trust declaration. Unknown historical values are null with reasons. |
| `artifacts` | POSIX relative path, byte size, media type and SHA-256 for each copied case/input/licence, observation, QPY, metadata, QASM, checker result, log and proposal artifact. No absolute paths. Excludes evidence itself and later render products. |
| `coverage` | Expected/observed IDs per side, missing/completed IDs, expected graph/angle cases, circuit-result links, classical-table sizes and excluded questions/reasons. |
| `circuit_results` | Actual checker results keyed by the exact `circuit-result-…` identity defined in §6; each lists every covered execution ID. |
| `checks` | All required check slots, including blocked ones. |
| `findings` | Grouped differences with their affected check and execution IDs and any model-claim references. |
| `run_state`, `evidence_summary`, `status_counts` | Derived under section 8, with all enum counts present even when zero. |
| `limitations` | Finite inputs, floating-point numerics, no optimizer/hardware/noise/dynamic/whole-program claim, trusted local execution and no independent attestation. |

Each check has `id`, `kind`, `scope_ids`, `required`, `status`, `reason_code`, `summary`, `expected`, `observed`, `metric`, `tolerance`, `artifact_refs` and nullable `circuit_result_id`. Unused fields are null, not omitted. Expected/observed values are JSON data, rendered as escaped text. Kind-specific validation enforces the criteria in section 8.

Each finding has `id`, `kind`, `check_ids`, `scope_ids`, `title`, `explanation` and `proposal_claim_refs`. IDs are stable kind names within this record; the evidence digest prevents a decision from drifting onto another run.

### Exact supporting record shapes

An observation document has schema `qref.qaoa-observations/v1` and required fields `side`, `case_sha256`, `observer_sha256`, `module_sha256`, `environment`, `started_at`, `finished_at`, `executions`, `classical_tables`, `errors`. Side is `reference|target`. Environment is `{python_version, os, architecture, distributions}`; distributions are sorted `{name, version}` records. A missing environment is null with a diagnostic reason, never a substituted current interpreter.

Each execution has `id`, `input_sha256`, `inputs`, `state`, `reason_code`, `started_at`, `finished_at`, `circuit`, `sampling`, `numeric`, `artifact_refs`, `error_ref`. State is `completed|failed|unsupported|incomplete|not_run`. Initialize all expected entries as not run. Atomically record an execution as incomplete before invoking it; a killed worker must not turn begun work into a fabricated completion. Final validation and report generation preserve that state.

- `circuit`: actual measured QPY artifact, JSON metadata artifact, measurement-free QASM artifact, qubit/classical dimensions, ordered register widths, raw terminal map, layout metadata, global phase and producer Qiskit version. Null when no circuit was captured.
- `sampling`: requested/completed shots, raw counts/count sum, backend class, recorded backend options and run kwargs. Counts and completed values are null when unavailable, not zero. Serialize JSON-safe option values; record an unsupported value's qualified type and the missing scope instead of executing an arbitrary repr or claiming its value was captured.
- `numeric`: returned scalar, module objective on its captured counts, exact probabilities and module objective on those probabilities. The parent computes independent expected values; worker output is not the independent oracle.
- `classical_tables`: one entry per graph, containing n and every basis assignment's module `maxcut_obj` result plus its one-hot `compute_expectation` result. The parent checks the independent negative-cut rule.

Validate finite values, binary count-key widths, nonnegative integer counts, positive totals, probability dimensions/mass and declared graph dimensions. Nulls require a failed/unsupported/incomplete context. Unsupported measurement/layout data blocks dependent interpretation rather than being projected under a guessed map.

Evidence provenance has required fields `tool_version`, `tool_revision`, `observer_sha256`, `comparison_sha256`, `reference_sha256`, `target_sha256`, `reference_pins_sha256`, `target_pins_sha256`, `source_receipts`, `started_at`, `finished_at`, `reference_environment`, `target_environment`, `proposal_refs`, `trusted_local_code`, `unknown_reasons`. Each source receipt copies the case declaration and adds `module_sha256`, `license_artifact` and `license_sha256`. Unavailable tool metadata is null with its field named in `unknown_reasons`; source/licence fields required for a public release cannot be invented. No runtime Git lookup is required. New run timestamps are actual UTC.

The **successful** proposal record has schema `qref.proposal/v1`, `mode`, reference/output/prompt/schema SHA-256 values, actual start/end times, CLI version, sanitized fixed argv, authentication category without account identity, resolved model, result category `success`, usage, `cli_estimated_cost_usd`, the four-field `output`, and copied artifact references. Failure uses the separate error schema in §5, not nullable success fields. Preserve a raw response only after privacy review. Never publish tokens, account email/organization ID, home-directory paths or inferred timestamps.

The checker configuration uses the exact digest fields in §6. Preserve raw checker/configuration artifacts when exposed by the pin; otherwise record default-call provenance and missing details explicitly. An input digest with shots is **not** a circuit-result digest.

Write evidence once as sorted-key UTF-8 JSON with LF line endings, `allow_nan=false`, two-space indentation, `ensure_ascii=true` and one final LF. Record identity is SHA-256 of **those exact bytes**, not a parse-and-reserialize operation. Input digests separately use compact canonical JSON as defined above. Hashes establish consistency, not a trusted signer or timestamp.

### Human overlay: `qref.decisions/v1`

Required fields: `schema`, `evidence_sha256`, `decisions`. Each decision has `finding_id`, `decision`, `reviewer`, `reason`, `recorded_at`.

Decisions are `accepted_intentional`, `rejected` or `needs_review`. Any recorded decision requires nonempty self-reported reviewer/reason and UTC RFC3339 time. A template may contain `needs_review` with **all three null**; that means unrecorded, not a person asking for review. Partial identity/reason/time is invalid. Missing findings are also unrecorded. Reject duplicates, unknown IDs, wrong evidence digest and any attempt to bind a decision to an integrity/error check rather than a valid difference finding.

| Overlay condition | Finding label |
|---|---|
| No entry, or all-null template entry | `Not recorded` |
| Recorded `needs_review` | `Needs review`, with actual reviewer/reason/time |
| Recorded `accepted_intentional` | `Accepted as intentional`, without changing checks |
| Recorded `rejected` | `Change rejected`, without changing checks |

Derive display `review_summary` in this order: `rejected` if any finding is rejected; `pending` if evidence is incomplete or any finding is unrecorded/needs review; `accepted` if complete evidence has findings and all are accepted; `not_required` if complete evidence has no findings. Labels are respectively `Human review: changes rejected`, `Human review: pending`, `Human review: recorded acceptance`, `Human review: not required`. The seed's unrecorded state may say `Human decision: not recorded`. These are self-reported review states, not scientific verdicts or attestations.

Keep the evidence byte-for-byte unchanged across reviewed exports. A decision changes only the displayed human disposition and export manifest. Do not invent Severyn's acceptance from his approval of this project or from the model's notes.

### Export layout and integrity

A new run/export directory contains `evidence.json`, portable `case.json`, copied `artifacts/`, `review-template.json`, `index.html`, `manifest.json`, optional `decisions.json`, and `evidence.zip`.

Initial `run` finalization validates the frozen evidence/artifact graph before generating HTML, manifest or ZIP; it must not require an already rendered bundle. The internal writer operates once in the new directory owned by that run, then verifies the finished export. The public `report` command instead verifies an existing complete bundle before copying it to a new export. Both use the same renderer/manifest rules; no public allow-incomplete bypass is added. This distinction avoids a first-render verification cycle.

The manifest has schema `qref.manifest/v1`, evidence digest, optional decisions digest, render timestamp, renderer identity/hash and the relative path/size/SHA-256 of every exported file except itself and `evidence.zip`. Generate ZIP last, including the manifest and every listed file; never include ZIP in itself. This avoids self-hash cycles.

`verify-bundle` takes a directory, never extracts arbitrary archives, imports candidates or loads QPY. Reject missing/undeclared files, symlinks, absolute paths, backslashes, `.`/`..` segments and invalid record links. Check sizes/hashes/schemas. Then inspect `evidence.zip` **without extraction**: its unique regular member names must be exactly the manifest's files plus `manifest.json`; reject duplicate names, directories, links, encryption and unsupported compression. Stream every member, enforce declared byte limits and compare its bytes/digest with the verified directory, including the manifest itself. A corrupted or replaced ZIP must fail CI even when the loose files are correct.

Use maximum 1,024 files/members, 32 MiB per file, 256 MiB total uncompressed bytes and 1 MiB per diagnostic stream; modules/case/licence inputs are at most 256 KiB each. Bound decompression by actual emitted bytes, not only ZIP headers. Exceeding a limit is an explicit resource-limit validation failure, not permission to omit data. A moved directory must validate.

Hashes establish unsigned consistency, not publisher identity: replacing the record and every hash together is not detected. The CLI does not attest worker honesty. Do not show a seal or certification badge.

**Privacy is a publication gate, not a redaction feature.** If a bound log, path, source or response contains private material, do not publish that run or manually delete/edit its artifacts. Diagnose privately and produce a new inspected public-safe run with a new evidence identity. Pages publishes only an intact verified curated export; public omission must never masquerade as the original complete bundle.

## 10. Report behavior

The proposed surface is a **finding-first patch review document**, not a SaaS dashboard. It is a planning direction for review, not a claim that UI has been implemented or approved. The [report brief](docs/design/report-brief.md) and [browser-rendered schematic](docs/design/report-layout.png) define composition, copy, responsive behavior and accessibility. The editable [SVG source](docs/design/report-layout.svg) is also retained.

The first viewport answers what stayed the same, what changed and what needs a decision. For the seed:

> Equivalent circuits. A changed shot setting.
>
> The reference completed 1,024 shots. The target completed the requested shots. In the fresh probe, the prompt requested this correction and the model documented it before execution.

Show requested/reference-completed/target-completed values as a table. Keep the human state and a visible coverage sentence beside the result. Do not treat the reference's shot-request violation as a target defect.

Required document sections: Findings; Checks on declared inputs; Coverage and limits; Source changes; Evidence and reproduction. Source diff starts at the relevant shot hunk but offers full bundled source and license text. Nine-case tables link to exact observations. Show actual angle arrays and graph definitions. Preserve numerical values and tolerances in details.

The report must derive its finding from evidence, not hardcode the seed story. Identical programs that both ignore a request must say so. An incomplete comparison with a known difference must show both. A circuit-only or classical-only regression gets its own accurate summary. No observations, unsupported input and failed execution never become empty success states.

The static report has no Run, Migrate or Save approval button. Display `Recorded local execution`; distinguish proposal time, execution time, human decision time and report-generation time. If a historical execution time is missing, say not recorded, never use file mtime.

Required interactions are native section/evidence anchors, native disclosures, full-source access, HTML save/download and exact evidence-JSON export. JSON export can read an escaped `<pre>` containing the exact evidence text and create a local Blob; do not normalize the JSON or interpolate it into executable JavaScript. A no-script reader can still inspect/select all core facts and raw evidence. Native HTML download or browser Save As must work without an online API. Do not claim a browser-reserialized HTML copy has identical bytes to the manifest's original.

ZIP is produced by the CLI and published alongside the report. Its link is explicitly an accompanying-file/online download, not a payload embedded in a standalone HTML copy. A lone HTML file remains fully readable and can export its embedded evidence JSON; full bundle verification/reproduction uses the original export directory or downloaded bundle. Avoid a circular self-embedded ZIP.

Use explicit Jinja autoescaping and `StrictUndefined`. Only packaged trusted CSS/JS may bypass text escaping. Paths, code, logs, model notes and raw record strings remain text; use `textContent`, not `innerHTML`, for dynamic content. Add a restrictive meta CSP with no network connections, no objects/base/forms and only the fixed inline script hash. No remote fonts, CDNs, analytics, fetches, service worker or automatic external requests. Test script-delimiter and HTML-entity inputs in the actual browser. Jinja's template sandbox is not a Python execution sandbox and is not the product's security claim.

## 11. Deployment and publication

**Target:** project Pages site for `SeivenBell/tq-ledger`, expected shape `https://seivenbell.github.io/tq-ledger/`. This is a planned address, not a live-link claim. Use the actual deployment output URL as authoritative.

After review and a real successful run:

1. Inspect the chosen run for secrets, private paths, unreviewed claims and source rights. Publish only a curated real export under `examples/qaoa-run/`; generated working runs stay ignored.
2. Enable GitHub Pages with GitHub Actions as the publishing source. It is currently disabled. If permissions or environment approval block this, state the precise blocker; do not bypass protection or claim deployment.
3. Implement a `pages.yml` workflow. On main, use official checkout/configure-pages/upload-pages-artifact/deploy-pages actions. Resolve/pin their actual commit SHAs at implementation rather than inventing them here. Build and deploy are linked with `needs`; deployment uses `github-pages` environment and `pages:write`, `id-token:write`, `contents:read` permissions.
4. Build job: set up Python, install frozen **base** dependencies, verify the curated bundle, then copy its already generated export bytes into `site/`. CI does not rerender the report, call a model or execute a scientific candidate. No repository/auth secrets belong in the browser.
5. Upload **only `site/`**, never the repository root, archive, logs or `.claude` configuration. Include the actual public bundle/download files referenced by the page. Use relative asset/fragment/download URLs so the project subpath and local copies work.
6. Deploy the uploaded Pages artifact. Verify the actual URL anonymously on desktop/mobile, download the evidence, and confirm the page displays the same evidence digest as the curated record.

GitHub Pages supports static project sites; it is not a free hosted commercial SaaS backend. This open-source report does not perform transactions or collect form data. GitHub itself logs visitor IP addresses for security; do not claim that visiting the hosted page sends no data to its host.

No new domain, Render instance, database, Clerk, SurrealDB, Eon Era or Expo is needed. A local HTTP server is only a browser-inspection convenience; offline file opening remains an acceptance case.

## 12. Modules and repository organization

One Python package; no separate frontend application. Modules concentrate real behavior behind small interfaces:

| Module | Responsibility and seam |
|---|---|
| `contracts.py` + packaged schema | Parse/validate case, evidence, decisions and manifests; enforce cross-record identity and coverage. All callers use the same rules. |
| `proposal.py` | Auth-category guard, fixed Claude invocation, structured response validation, copied input/proposal artifacts. No code execution. |
| `execution.py` + private `_worker.py` | Host orchestration, deadlines and copied inputs; standalone observation/check workers for the actual two environments. |
| `checks.py` | Pure comparison, independent negative-cut interpretation, status mapping, expected check inventory and finding aggregation. |
| `report.py` + packaged template/CSS/JS | Validate and export readable evidence plus optional decisions. Does not import quantum libraries or execute source. |
| `__main__.py` | Parse command options and route to these interfaces; no scientific policy hidden in CLI wiring. |

Do not add a repository class, plugin manager, model-provider factory, event bus or generic adapter registry. The two interpreter environments are real variation; hypothetical future frameworks are not.

Proposed implemented tree:

```text
PRODUCT.md  CONTEXT.md  SPEC.md  PLAN.md  REVIEW.md  CLAUDE.md  README.md
pyproject.toml  uv.lock  .python-version
src/qref/                 # modules, private worker, schemas and report assets
cases/qaoa.json            # one supported workflow manifest
examples/qaoa-run/         # curated real public export, only after execution
tests/                    # behavior and negative fixtures; no seeded claim inflation
.github/workflows/        # focused checks and static Pages publication
evidence/qaoa/            # unchanged seed research evidence
docs/design/              # proposed report brief and schematic
docs/reviews/             # planning checks and review dispositions
archive/research-2026-10/  # abandoned directions and historical probes
```

The code/project/workflow paths above are future implementation outputs, not existing scaffolds. Root active instructions must not point implementers into the old Ledger queue. Keep the archive out of default build, test, package-discovery and site-upload paths.

## 13. Evaluation and release criteria

Implementation must exercise all rows below. Synthetic fixtures are labelled and isolated from real migration evidence.

| Scenario | Required observation |
|---|---|
| Real seed | Complete expected observations, actual submitted circuits, classical tables, grouped shot difference and prior model disclosure. |
| Clean modern control | Identical supported modern programs preserve the declared behavior; no legacy-shot violation contaminates this control. |
| Seeded rotation change | Circuit and/or exact numerical difference; not called a naturally observed model error. |
| Seeded sign/bit-order change | Circuit may remain equivalent; independent classical checks expose the changed interpretation on asymmetric inputs. |
| Shot policy | Changed setting and per-side request compliance stay distinct; accepting intent changes only review disposition. |
| Unsupported path | Mid-circuit measurement, changed map/layout, missing or multiple backend runs are explicit unsupported coverage, not silent pass. |
| Inconclusive checker | Timeout/probable/no-information/unknown criterion cannot become equivalent. Use deterministic private-seam fixtures for otherwise hard-to-trigger outcomes. |
| Pairing/metadata | Reordering is harmless; duplicate/missing IDs, wrong digests, stale proposal attribution and non-finite values cannot silently compare. |
| Runtime failure | Reference failure preserves useful target diagnostics; no retry or stale prior success. |
| Review binding | Wrong digest/unknown finding/duplicate decision rejected; accepted/rejected overlays leave execution evidence unchanged. |
| Portable export | Moved directory verifies; missing/altered/undeclared files or unsafe paths fail. Browser JSON download matches exact evidence bytes. |
| Offline/XSS/accessibility | Core report works without network/JS; scripted exports work with JS; escaped hostile strings remain inert; keyboard/mobile/zoom usable. |

Permanent tests must catch plausible consumer bugs and status transitions. Do not test source wording, configuration copies, mock forwarding, incidental defaults or non-empty output. Actual CLI execution and actual browser inspection are required release evidence, not replaced by tests.

A fair baseline is the model's own notes plus raw QCEC/Aer output. Can a reader identify the change, its prior disclosure, the checker scope, the reference's deviation and the remaining decision? Without an independent reviewer, report only a checklist-based demonstration, not time savings or validated usability.

### Two-minute demonstration

Show the real reference/target and recorded proposal, run the local comparison, open the generated report, inspect the shot difference, explain why equivalent circuits do not settle sampling behavior, and show coverage/source evidence/export. If showing a seeded decoder regression, label it explicitly. State that the public page displays recorded results. Disclose the old notebook and QCEC dependency. End with the real public URL, not a promise of a future platform.

### Hard stop conditions

Do not submit claims of a complete product if the fresh run, report export, actual public surface or required evidence is missing. Do not manufacture a failing example, hide an unsupported path, silently substitute recorded results for a new run, or wait indefinitely for an unanswered email. If a proposed capability cannot meet its criterion, revise the spec with the owner before implementation silently shrinks it.

## 14. Risks and review decisions

| Risk | Decision/mitigation |
|---|---|
| Thin wrapper rather than a new market | Present a bounded open-source review workflow; adoption remains a hypothesis. |
| Original reference contains a bug | Separate preservation from independent declared interpretation and human intent. |
| Observer inspects unused builder output | Capture the actual Aer submission; positive feasibility is now exercised. |
| Generic migration promise exceeds the case | One helper interface, explicit small input limits, unsupported state. |
| New/old dependency conflict | Two environments, actual metadata, no runtime resolver/fallback. |
| Unfunded model/backend | Existing subscription path exercised; free static host; no hosted model feature. |
| Forged provenance impression | Exact hashes are consistency checks, not attestations; reviewer label self-reported. |
| Planning documents mistaken for software | Root status, review gate and all future commands explicitly identified. |
| Deadline scope | No new platform features or optional UI controls. Finish the required path and recording before visual extras. |

The external reviewer must challenge status/inventory consistency, evidence binding, CLI/auth behavior, observer coverage, independent decoding, portable export and deployment truth. UI appearance cannot compensate for a missing end-to-end path. See [REVIEW.md](REVIEW.md).

## 15. Sources and reading depth

Read on 2026-10-25 unless a prior research date is stated. `Full` means the named page/artifact, not every linked document. No abstract-only paper supports a new claim here.

| Source | Depth and use |
|---|---|
| [Ultraplan status](https://code.claude.com/docs/en/ultraplan) | Full. The named preview and keyword were removed; this package uses independent planning reviews, not a claim that the removed mode ran. |
| [Claude CLI reference](https://code.claude.com/docs/en/cli-reference) | Partial: commands and relevant flags, authentication status, tools/MCP, restricted mode, settings sources, structured output. Exact invocation exercised locally. |
| [Programmatic Claude](https://code.claude.com/docs/en/headless.md) | Partial: basic usage, bare-mode authentication, structured output and session metadata sections. Establishes why `--bare` is excluded. |
| [Structured outputs](https://code.claude.com/docs/en/agent-sdk/structured-outputs.md) | Partial: quickstart, supported schema dialect/configuration and validation caveats. Proposal shape exercised. |
| [Settings reference](https://code.claude.com/docs/en/settings-reference.md) | Partial: relevant settings index entries; actual inline configuration accepted by tested CLI. No claim of a full managed-policy audit. |
| [QCEC equivalence guide](https://mqt.readthedocs.io/projects/qcec/en/stable/equivalence_checking.html) | Full returned guide. Checker guarantees differ; newer living-document interfaces are not assumed available in the pin. |
| [Quantum workflow source audit](archive/research-2026-10/docs/research/round2/quantum-workflows.md) | Relevant methods/results, incumbent capabilities and verified artifact sections read; its source register records paper methods and experimental setup. |
| [Runtime source audit](docs/reviews/planning-verification.md) | Captures independent design input, actual positive probes and limits. Versioned package metadata and installed Aer class declarations were inspected by the runtime-design agent. |
| [Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits), [what Pages is](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) | Full each. Static hosting, action/permission requirements, limits, site URL and host IP logging. Repository metadata confirms public/Pages-disabled prerequisite only. |
| [Jinja API](https://jinja.palletsprojects.com/en/stable/api/) | Partial: Environment, autoescape and undefined handling. Renderer behavior still requires implementation/browser checks. |
| [jsonschema validation](https://python-jsonschema.readthedocs.io/en/stable/validate/) | Partial: validator protocol, draft selection and format-validation caveats. Use explicit Draft 7 and semantic checks. |
| [Jinja 3.1.6 metadata](https://pypi.org/pypi/Jinja2/3.1.6/json), [jsonschema 4.25.1 metadata](https://pypi.org/pypi/jsonschema/4.25.1/json) | Release metadata/version/Python/dependencies read. Metadata is not proof of installed renderer behavior. |
| [Original notebook](https://github.com/qiskit-community/qiskit-textbook/blob/0ae905083ec3872d7ddc6bb4001d5468f476d93f/content/ch-applications/qaoa.ipynb) | Earlier investigation inspected all code cells; helper subset executed. Included Apache-2.0 license read. The old source is a fixture, not evidence of current maintainer demand. |

The one unanswered inquiry concerned benchmark reporting, not SDK migration. It neither validates nor invalidates this product's demand. Further outreach remains unauthorized.

# Planning verification and limits

This record concerns the QRef specification and its feasibility probes. It is not a product test report, completed application or public deployment claim.

## What the user authorized

The user chose a working AI × quantum submission, accepted the bounded migration-review direction, requested repository archiving and a complete specification for another AI to review before implementation. Stack selection was delegated; no new paid services were allowed. One research inquiry was sent with no reply. Additional outreach is not authorized.

## Literal Ultraplan status

Anthropic's [official page](https://code.claude.com/docs/en/ultraplan), read in full, says the `/ultraplan` preview, keyword and web refinement option were removed. No claim is made that this removed mode ran. The planning work instead used independent runtime/UX analysis, concrete capability probes and a specification review process.

## Independent design inputs

- **RuntimeContract:** inspected the source/target helpers, old observer, recorded data, installed Aer inheritance and official Qiskit/QCEC/package metadata. Proposed the execution, independent decoding, status, coverage, integrity and review-overlay contract. It performed no runtime tests. Its most important correction was to capture actual submitted circuits, not a separately rebuilt circuit.
- **ReportUX:** read the product truth, source notes and relevant evidence plus design/writing guidance. Proposed a finding-first offline report, explicit human state and coverage, source/evidence links, accessible layouts and scope cuts. It wrote no product UI. The visual brief remains a proposal for review.
- **ArchiveHistory:** moved the frozen 62-file manifest without changing source text. The integration owner then independently checked exact Git blob identities and executable modes.

These inputs challenged the plan; they are not the next external review requested by the user. That review uses REVIEW.md and records its findings separately.

## Fresh capability probes

Source and results are preserved at [immutable probe revision 67db6c5](https://github.com/SeivenBell/tq-ledger/tree/67db6c595927faa91a85f64a7d1845f1c89b09dc/prototypes/qref-spec-probes). The branch is `research/qref-spec-probes`. It contains throwaway proof code, not production QRef.

### Subscription proposal

Observed authentication category: logged in through `claude.ai`, first-party provider, Pro subscription. No alternate API-key/provider billing environment flag was present. Account identity and secrets were not published.

Claude Code version: **2.1.308**. The exact successful argv is in [proposal-record.json](https://github.com/SeivenBell/tq-ledger/blob/67db6c595927faa91a85f64a7d1845f1c89b09dc/prototypes/qref-spec-probes/proposal-record.json). In structural form:

```text
claude --restricted -p --model sonnet --effort high
  --tools "" --strict-mcp-config --mcp-config '{"mcpServers":{}}'
  --disable-slash-commands --no-session-persistence --setting-sources ""
  --settings FIXED_RESTRICTIVE_SETTINGS_JSON
  --output-format json --json-schema PROPOSAL_OUTPUT_SCHEMA
```

The settings requested disabling hooks, auto memory, CLAUDE.md discovery, Claude.ai connectors and synced plugins/skills. The call succeeded, but that result is not an attestation that every initialization source or managed policy was absent. It ran from a new temporary directory with source text on stdin, without bare mode, a public web backend or an API key.

The CLI returned transport exit 0, result subtype `success`, `is_error=false` and structured fields `code`, `summary`, `intentional_changes`, `uncertainties`. Resolved model: `claude-sonnet-5-5`. One invocation took approximately 21 seconds and reported two SDK turns. Its roughly $0.045 estimate is a client estimate, not an invoice or proof of a billing debit.

The generated source was inspected before execution. The prompt explicitly supplied the previously known 1,024-versus-512/17 behavior and requested a disclosed correction. The model complied. Its uncertainty about direct Aer submission was preserved, then tested separately. This establishes an instructed port and execution corroboration, not autonomous discovery, hidden-error detection or an unbiased performance trial.

Official [headless documentation](https://code.claude.com/docs/en/headless.md), read through basic/bare/structured-output sections, states that `--bare` skips subscription OAuth/keychain authentication. This is why the tested path deliberately avoids it.

### Actual submitted-circuit capture

The positive probe used the pinned reference/target environments and a scoped `AerBackend.run` class hook. It retained actual submitted circuits, counts and identity measurement maps. It compared returned values against independent negative-cut decoding of those same counts.

| Observed measure | Result |
|---|---|
| Reference executions | 18 |
| Target executions | 18 |
| Independent classical basis assignments per side | 64 |
| Distinct actual submitted circuit pairs | 9 |
| Captured-circuit QCEC results | All nine `EquivalenceCriterion.equivalent` |
| Reference completed shots | 1,024 for both declared requests |
| Target completed shots | Requested 512 or 17 |

The [capture script](https://github.com/SeivenBell/tq-ledger/blob/67db6c595927faa91a85f64a7d1845f1c89b09dc/prototypes/qref-spec-probes/capture_probe.py), [comparison script](https://github.com/SeivenBell/tq-ledger/blob/67db6c595927faa91a85f64a7d1845f1c89b09dc/prototypes/qref-spec-probes/compare_probe.py), generated target, reference and result JSON are complete primary artifacts. They are easy to rerun with the included requirements.

This proves the positive mechanics for the seed. It does **not** prove the proposed production observer, record schema, failure semantics or complete input range. The throwaway capture imports the already inspected module before installing its hook; import-time interception remains an implementation acceptance requirement. Its assertions and positional pairing are not the production validation design.

## Deployment checks

Authenticated repository metadata showed `private=false`, `has_pages=false`, default branch `main`. The repo can serve the planned public open-source artifact, but Pages enablement and deployment have not been performed by this planning task.

The official Pages [workflow guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) and [overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) were read in full. They support a static project report, specify action/permission/environment requirements and describe host IP logging. They do not provide a free runtime for Python/model execution.

The public address in SPEC is a planned URL shape. Only an actual deployment output and anonymous browser check can establish the live URL.

## Dependency evidence

The runtime-design agent inspected versioned PyPI JSON for Qiskit/Aer/QCEC/NumPy/NetworkX and source declarations for both Aer backend classes. Its observations are reflected in SPEC's pin table; it did not perform a clean Linux reinstall.

Jinja 3.1.6 metadata and its complete BSD-3-Clause [license](https://raw.githubusercontent.com/pallets/jinja/3.1.6/LICENSE.txt) were read. The release tag resolves to `15206881c006c79667fe5154fe80c01c65410679`, dated 2025-03-05. This release is older than 18 months and may be stale; the current PyPI release endpoint also reports 3.1.6. Recheck advisories during implementation. It is an infrastructure pin, not current market evidence, and metadata does not certify renderer behavior.

jsonschema 4.25.1 metadata and its complete MIT [license](https://raw.githubusercontent.com/python-jsonschema/jsonschema/v4.25.1/COPYING) were read. Release tag `331c38425519b69118d22ebe467ad230fb83a010` is dated 2025-08-18. Validation docs were read for draft selection and the limits of format validation.

The earlier Qiskit textbook source is deliberately stale fixture material. It is not evidence that an active maintainer currently wants this migration.

## Repository archive checks

All **62** source paths from snapshot `33262ed1e9e2fa99d8da84c4f6a814d3a26bfa34` were moved under `archive/research-2026-10/` with the same relative paths. The integration owner checked every destination's Git blob hash against that snapshot and confirmed the old paths were absent. Both shell scripts retained executable mode 0755. Both supplied original Fable texts remain unchanged.

The selected 14-file QAOA seed was retained under `evidence/qaoa/`. The archive index points to immutable history rather than claiming historical main-path links are current. No root-level compatibility stubs were left at abandoned paths.

## Layout capture

The proposed layout SVG was rendered in a real browser and captured as `docs/design/report-layout.png`; the image is a labelled design schematic, not application verification. A standalone SVG raster preview had a theme/contrast failure, so the readable browser capture is the primary preview. Actual responsive/product UI checks remain implementation acceptance work.

## Follow-up capability checks

The follow-up source and results are at [revision 57af049](https://github.com/SeivenBell/tq-ledger/tree/57af049088e3df9e18e1fbde883ec3525e4f1ea7/prototypes/qref-spec-probes). Read depth: full probe sources and observed JSON outputs. These do not implement QRef.

| Scenario | Actual result | Boundary |
|---|---|---|
| Identical one-qubit circuits | `equivalent` | Default pinned QCEC entrypoint only. |
| Gate-level global minus sign | `equivalent_up_to_global_phase` | Confirms the retained global-phase mapping. |
| Relative Z change | `not_equivalent` | A relative phase is not accepted as a global phase. |
| Qiskit global-phase metadata only | `equivalent` | Tested import path ignored it; do not call QASM2 lossless. |
| Native QPY roundtrip | Circuit and nonzero global phase retained in both 0.46.3 and 2.6.1 | Same-runtime, two-qubit example; not cross-version loading or integrated capture. |
| Clean-environment authentication status | Exit 0, logged-in `claude.ai`, `firstParty` | No model request in this follow-up; combined clean-environment generation remains Gate C acceptance. |

The pinned [binding file](https://github.com/munich-quantum-toolkit/qcec/blob/v3.11.0/bindings/register_equivalence_criterion.cpp), [criterion definition](https://github.com/munich-quantum-toolkit/qcec/blob/v3.11.0/include/EquivalenceCriterion.hpp) and [alternating checker](https://github.com/munich-quantum-toolkit/qcec/blob/v3.11.0/src/checker/dd/DDAlternatingChecker.cpp) were each read in full. The binding descriptions invert the two phase explanations. The checker implementation explicitly emits `EquivalentUpToGlobalPhase` for a non-one global weight on the identity; the direct runtime result agrees. A proposed swap based only on the binding prose was rejected.

An initial phase-probe child inherited a protected workstation cwd and failed at import. Running the same source from the explicit accessible probe directory succeeded. This is an execution-environment correction, not a hidden quantum/model defect. Observation/proposal workers must use explicit owned working directories.

## Internal challenge dispositions

Two additional read-only reviewers challenged the drafted package. One initially marked the contract blocked; the other marked it suitable for external review with implementation blockers. Their reports were not external owner approval. The integration owner made the following decisions before this handoff:

| Finding | Resolution |
|---|---|
| Claimed reversed QCEC phase mapping | Rejected the proposed swap after reading pinned checker source and exercising global/relative phase cases. Retained conservative enum mapping and recorded the docstring trap. |
| Overlapping run, evidence, headline and exit states | Added ordered precedence, completed-pair definition, failure/check matrix and explicit diagnostic-versus-corrupt-bundle behavior. |
| Integrity error could share intentional shot approval | Only valid differences create findings. Sampling-integrity errors invalidate evidence and cannot receive accept-intent decisions. |
| Proposal failure lacked a schema/commit boundary | Added separate proposal-error schema, incomplete checkpoint and last-written runnable case marker. |
| Source/licence/run identities were incomplete | Added bound per-side source receipts, extraction/licence artifacts, exact original/portable case hashes and evidence-digest run identity. |
| Circuit identity could accidentally include shots | Froze the QASM-pair/configuration digest and explicitly excluded shots. Added opaque measured QPY plus metadata alongside lossy analysis QASM. |
| Authentication guard was underspecified | Defined command, accepted categories, environment rules and deadlines; exercised the clean status guard. No billing/managed-policy attestation claimed. |
| ZIP was not protected by loose-file verification | Require member-name/byte verification without extraction, resource limits and failure on a replaced ZIP. |
| Public/private diagnostic conflict | Abort publication of that run; never delete/redact a bound artifact and call it the same evidence. |
| Model disclosure sounded independently discovered | Explicitly disclose that the fresh prompt supplied the known shot issue and requested correction. |
| Review states omitted recorded needs-review/clean outcomes | Added complete labels and separated all-null templates from actual recorded decisions. |
| Execution/report gate dependency cycle | Gate B provides labelled contract fixtures; D emits core evidence, E builds reporting, F integrates the real first export. Initial rendering does not require a pre-existing rendered bundle. |
| Old research receipt had no production-format replay binding | Curated release must use a fresh implemented proposal, then preserve it for recorded replay; old case attribution stays null. |
| Schematic clipped header and omitted run metadata | Rebuilt from the exact top-left capture region and added explicit not-recorded identity/time rather than fake values. |
| Half-day constraint absent from active plan | Restored it as an explicit review gate. No completion guarantee or silent scope cut; owner decides if the full path does not fit. |

The package is ready for the **requested external specification review**, not approved for implementation. Deadline fit remains a disclosed planning risk; the probe does not measure build duration. All named release acceptance criteria remain required unless the owner explicitly changes them.

## Still unimplemented

All production commands, packaged schemas, complete observer/error protocol, renderer, export validator, review overlay, curated release record, CI, public site, final browser checks, video and submission remain implementation work. The proposed eight-qubit range and negative/failure scenarios are acceptance requirements, not completed experiments.

Do not turn the positive probes into a success rate, a claim of catching hidden model mistakes, a customer commitment, an independent attestation or a probability of winning.

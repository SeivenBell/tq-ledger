# Review and release 0.1 record

Date: 2026-10-26. Reviewer and implementer: the same AI session (Claude). This is **not** an independent review; Gate A's "fresh reviewer" condition is unmet and is stated here rather than hidden.

## Review verdict on the planning package

**Blocked as written, ready after an owner scope decision.** The contracts were implementable without inventing core semantics. One blocker remained: the full acceptance path could not fit the owner's actual window (two hours total, including review). Per PLAN.md, the owner chose the scope:

> Core vertical slice: `qref propose` (real subscription call), `qref run` (both pinned envs, actual Aer capture, QCEC + classical + shot checks, ordered statuses), static finding-first HTML + exact evidence JSON + manifest, `qref verify-bundle` (hashes only), key negative tests, and a real export deployed to GitHub Pages. Defer: ZIP, decision-overlay re-export, the full fixture matrix and the recording.

The owner also approved enabling GitHub Pages.

## Implemented and exercised

| Capability | Evidence |
|---|---|
| `qref propose` | Three real calls via the existing claude.ai Pro login, Claude Code 2.1.308, `claude-sonnet-5-5`, no API key. Auth-category preflight, billing-override refusal, env allowlist, 180 s deadline, schema + `ast.parse` validation, error checkpoint, `case.json` written last. Each call took about 25 s. |
| `qref run` | Seed and model-generated ports run in Qiskit 0.46.3 / 2.6.1 pinned environments in about 5 s. All 18 executions per side were captured at the actual `AerBackend.run` call (hook installed before import), with QPY, metadata and measurement-free QASM. Nine distinct submitted-circuit pairs were all `equivalent`. 277 checks: 241 pass, 36 difference, grouped into one `shot_policy` finding. |
| Status rules | Ordered `invalid → failed → partial → complete`. Shot-integrity errors invalidate the run and are never findings. Interrupted or failed workers are not completed pairs. Exit codes 0/1/2. |
| Report | No-JavaScript, self-contained HTML with a strict CSP (hashed inline CSS only). Finding first, shot table, model disclosure separate from observations, `Human decision: not recorded`, coverage, limits, a diff with shot hunks first, full sources, receipts, licence and reproduction steps. Checked in a browser at desktop width and in a 375 px frame. |
| `qref verify-bundle` / `qref report` | Manifest hash/size checks. Rejects undeclared, missing or changed files, unsafe paths and symlinks. Checks the evidence digest and every evidence artifact. Verifies the template binding. `report` re-renders only a verified bundle. |
| Tests | 24 behaviour tests: status precedence, integrity, pairing, QCEC mapping, case rejection, duplicate keys/NaN, a **seeded decoder regression caught while circuits stay equivalent**, hostile-title escaping, tamper/undeclared-file detection, the trust flag, stale proposal attribution, and decision overlays (applied, tampered, unknown finding, partial fields, bad timestamp, wrong evidence). |
| Decision overlay (added in the second hour) | `qref report --decisions` validates `qref.decisions/v1`, binds it to the exact evidence digest, refuses decisions on unknown findings, renders the SPEC label mapping and leaves `evidence.json` byte-identical. `verify-bundle` checks the decisions digest. |
| Examples | `examples/seeded-decoder` is a labelled seeded regression: all circuit checks pass and QRef reports the classical-helper, weighting and returned-value differences. `site-src/examples.html` links all three published examples. |
| Fresh setup | The documented setup commands built new pinned environments in a second clone on macOS; tests and a seed run passed there. Linux remains unproven. |
| Pages | `.github/workflows/pages.yml` verifies the curated bundles with base-only install, then uploads only `site/`. |

## A real observation from release work

The same no-hint prompt was sent to Sonnet four times before submission. Two ports **fixed** the ignored shot request (`shots=shots`) and disclosed it. Two **deliberately preserved** the effective 1,024 shots and said so. QRef reports these outcomes differently:

- The research port in `examples/research-port`, which honours requests: **"Shot setting changed"**. Reference and target complete different numbers of shots.
- The published fresh port in `examples/qaoa-run`, which preserves behaviour: **"Requested shot count not honoured"**. Both sides agree, so whether to fix the request is a review decision.

This is three samples, not a rate. It does show why the model's statement and the execution evidence must stay separate: identical requests produced different behavioural choices.

## Deviations from SPEC (accepted for 0.1)

- Both candidate runtimes are explicit `.qref/envs/*` interpreters, and QRef's own install has no quantum extra.
- The first proposal (`proposal-001`, shot fix) was **not published**. It predates response sanitization (`session_id`), so it was regenerated rather than edited. That later call chose to preserve behaviour, so the curated public example shows the preserving port. The shot-fixing behaviour appears in the research-port example.
- The proposal record stores a sanitized `response.json` without `session_id` and `uuid`, and records which fields were removed.
- The evidence JSON is linked as a sibling file, not exported by in-page JavaScript, because the report ships no script.
- The worker records an explicit circuit-capture `layout` string rather than a structured layout.

## Deferred, not done

- `evidence.zip` and ZIP member verification.
- The full Gate D/E matrix: eight-qubit case, isolated-node case, clean modern control, seeded rotation change, unsupported map/control/extra-run fixtures, deadline and missing-runtime end-to-end runs, every review label, file-protocol/JS-off/zoom/keyboard audit and forced colours.
- Fresh Linux reproduction of the reference environment. CI verifies bytes only and never executes candidates.
- The two-minute recording itself (script: `docs/submission/demo-script.md`; runner: `scripts/demo.sh`).
- An independent review by a fresh AI. `REVIEW.md` still applies.

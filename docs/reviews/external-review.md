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
| Tests | 48 behaviour tests: status precedence, integrity, pairing, QCEC mapping, case rejection, duplicate keys/NaN, a **seeded decoder regression caught while circuits stay equivalent**, hostile-title escaping, tamper/undeclared-file detection, the trust flag, stale proposal attribution, and decision overlays (applied, tampered, unknown finding, partial fields, bad timestamp, wrong evidence), a replaced ZIP, a gate after measurement (reported as unsupported with exit 2, never a pass) and an import failure (failed run with the traceback kept), a worker deadline (process group killed, nothing fabricated) a missing interpreter (reported, never substituted), checker timeout and budget exhaustion (inconclusive, never equivalent), a seeded rotation change (circuit difference), a second backend run, a reversed measurement map and a control-flow block (all unsupported, never a pass), every review label, and proposal gatekeeping through a stand-in CLI (billing override and non-subscription login refused before any model call; refusals, unstructured output, bad syntax and CLI errors leave an error record and never a runnable case). |
| Decision overlay (added in the second hour) | `qref report --decisions` validates `qref.decisions/v1`, binds it to the exact evidence digest, refuses decisions on unknown findings, renders the SPEC label mapping and leaves `evidence.json` byte-identical. `verify-bundle` checks the decisions digest. |
| Examples | `examples/seeded-decoder` is a labelled seeded regression: all circuit checks pass and QRef reports the classical-helper, weighting and returned-value differences. `site-src/examples.html` links all three published examples. |
| Fresh setup | The documented setup built new pinned environments in a second macOS clone. `.github/workflows/test.yml` does the same on Ubuntu from scratch on every push: both pinned runtimes, the full test suite and a real seed run (complete, one `shot_policy` finding, all circuits equivalent). It passed on its first run. |
| Standalone page | Each report embeds the exact evidence text; a 20-line script, pinned by its SHA-256 in the Content-Security-Policy, saves it as `evidence.json` (checked in a browser: same length as the file). Without JavaScript the raw record is still readable in the page. `qref run` now prints a terminal summary of state, circuits, checks and findings. |
| Report detail | Per-execution table for both sides: state, requested/completed shots, returned objective next to the independent decoding, top counts and links to the captured QASM, QPY and metadata. The shot finding lists the model's statements that mention shots. |
| More examples | `examples/seeded-rotation` (labelled): a halved mixer angle that QCEC reports as non-equivalent, alongside the decoder case that only the classical checks catch. |
| ZIP bundle (third hour) | Every export now includes `evidence.zip` (all manifest files plus the manifest, never itself). `verify-bundle` streams each member without extracting it, checks names, duplicates, links, encryption, compression method and size limits, and compares bytes with the verified directory. A replaced ZIP fails even when loose files are intact (test). |
| Positive control (third hour) | `examples/positive-control` runs the same port on both sides, including an 8-qubit graph with an isolated node: 189 checks pass, no findings, exit 0. |
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
- The worker records an explicit circuit-capture `layout` string rather than a structured layout.

## Deferred, not done

- A full manual accessibility audit. Done so far: skip link is the first focusable element, every table header has a scope, every scrolling region has a label, there is one h1 and `lang` is set, and the report fits at 320 px (shot table fixed for narrow screens). Not done: screen-reader pass, 400% zoom and forced-colours inspection.
- The two-minute recording itself (script: `docs/submission/demo-script.md`; runner: `scripts/demo.sh`).
- An independent review by a fresh AI. `REVIEW.md` still applies.

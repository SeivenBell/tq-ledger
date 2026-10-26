# Review QRef before implementation

This repository contains a specification and executable research evidence, not a finished product. The user requested an independent AI review before implementation. Internal design reviews already informed the package; they do not stand in for that next review or authorize coding.

## Copy this prompt to the reviewing AI

```text
Review this QRef specification for implementation readiness. Do not implement the product.

Read CLAUDE.md, PRODUCT.md, CONTEXT.md, SPEC.md, PLAN.md, docs/design/report-brief.md, and docs/reviews/planning-verification.md. Inspect the retained evidence and the linked feasibility-probe source when a claim depends on it. Distinguish exercised mechanics from proposed behavior. Do not assume the proposed CLI, schemas, UI, package or deployment already exists.

The selected task is a bounded Qiskit/Aer migration reviewer: real local model proposal, inspected trusted Python execution in two pinned environments, independent submitted-circuit/classical/shot checks, immutable evidence, separate human decisions, portable HTML and free public hosting. Stack choice was delegated. No new paid services, public code execution, arbitrary notebook revival, hardware or general certification. The priority is a working AI x quantum submission, not new market discovery.

Challenge these points:
1. Does the workflow complete a useful review task without claiming scientific or whole-program correctness?
2. Are reference preservation, per-side interpretation, circuit outcomes, sampling settings, coverage and human intent kept distinct?
3. Do observation/check IDs remain well-defined during missing data, unsupported input, import failures and timeouts?
4. Can the exact contracts be implemented without inventing field meanings, status precedence, hash scopes or CLI behavior?
5. Does capture observe the actual Aer submission and returned result, rather than an unused reconstructed circuit? Is classical interpretation independently checked?
6. Can the subscription-only no-tools model path work without bare-mode/API billing or silently replaying recorded output?
7. Can the renderer verify records and work offline without quantum imports, unsafe HTML, mutable browser-only approval or self-hash cycles?
8. Are the export, review overlay and static GitHub Pages deployment truthful, portable and complete?
9. Can the complete critical path fit the user's roughly half-day build window without reviving Ledger, inventing a platform or silently dropping acceptance? If not, name the scope/schedule decision the owner must make; do not make it implicitly.
10. Does the proposed first screen explain the real difference and limits to a reader who has not read Python?

Use primary sources for disputed capabilities. State actual reading depth and distinguish an unrun acceptance requirement from a proven result. Do not rerun the user's reported failures just to confirm them. Do not spend the remaining build period on new market research or unrequested features.

Read the internal challenge dispositions in docs/reviews/planning-verification.md. In particular, the pinned QCEC binding docstrings contradict its checker source and the observed global-phase probe. Do not repeat the rejected enum swap without stronger counter-evidence. These internal checks do not replace your independent review or authorize implementation.

Write docs/reviews/external-review.md with prioritized findings. Each finding needs severity, exact file/section, affected user behavior, evidence and a concrete resolution. Distinguish blockers from optional improvements. If you edit a contract, update every affected active document together; do not leave conflicting versions.

Finish with one disposition: ready for implementation, ready with explicitly named non-blocking risks, or blocked by enumerated decisions. List what you actually exercised and what remains untested. Stop after review. No product code, deployment, mail, purchase, pull request or implementation issue creation unless separately authorized.
```

## What counts as a blocker

- A route to false equivalence/approval, fabricated coverage or a hidden scientific-scope claim.
- Unacknowledged arbitrary Python execution, leaked credentials/private data or unsafe rendering.
- A required paid service or unavailable authentication dependency.
- Ambiguous core input/output/status/hash semantics that would force implementers to make conflicting decisions.
- A proposed output that cannot be reproduced/exported/deployed as described.
- A minimum scope that cannot form a complete bounded workflow without silently dropping required behavior.

Lack of market validation is a disclosed project risk, not permission to restart product discovery. A seeded fixture is valid test evidence when labelled; it is not an observed agent error. An unanswered email is neither rejection nor adoption.

## Review completion record

The reviewer records its actual findings, changes and disposition in `docs/reviews/external-review.md`. That file is intentionally not pre-created with fake approval. If there are blockers, record the exact decision/input needed and finish all reachable review work. The owner authorizes implementation after reviewing the outcome.

## Separate prompt for implementation after approval

Use only after the review has no unresolved blockers and implementation is explicitly authorized:

```text
Implement the approved QRef specification in SPEC.md, following PLAN.md. Read CLAUDE.md, PRODUCT.md, CONTEXT.md, docs/design/report-brief.md and the external review first. Treat the approved report brief as the visual direction; do not restart a branding exercise.

Complete the bounded local proposal -> inspected execution -> independent checks -> human-review input -> portable report workflow. Use the selected single Python toolchain and free static hosting. Do not add unapproved platform features or interpret archived documents as current requirements.

Freeze contracts before parallel implementation. Give each module an owner; run consolidated checks after shared edit waves. Use real inspected source, actual model/run metadata and the actual submitted circuit. Preserve unsupported/inconclusive states and exact evidence identity. Do not fabricate human acceptance or imply that a static page executes a model.

Exercise all named acceptance scenarios, then the actual local CLI and public/offline desktop/mobile report. Deploy only a verified curated export; obtain the real public URL and record the real workflow. Update documentation to achieved behavior. Do not claim completion from test results alone or leave core work as stubs, placeholders or promised follow-ups.
```

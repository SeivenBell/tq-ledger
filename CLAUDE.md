# QRef

Selected project: bounded quantum-code migration review. Current phase: specification review. The user authorized planning and archiving, not product implementation.

## Route the work

For independent review, follow `REVIEW.md`, then read `SPEC.md`, `PRODUCT.md`, `CONTEXT.md` and `PLAN.md`. Record concrete findings and stop before implementation.

For separately authorized implementation, follow the approved `SPEC.md` and `PLAN.md`. The report brief at `docs/design/report-brief.md` defines the proposed/approved surface; do not restart product discovery or silently widen its scope.

For actual proof and missing capabilities, read `docs/reviews/external-review.md` (release 0.1: implemented, deviations, deferred) and `docs/reviews/planning-verification.md`. Code is in `src/qref/`; tests in `tests/`; curated public exports in `examples/` (regenerate, never hand-edit; `qref verify-bundle` must pass). Retained seed evidence is under `evidence/qaoa/`. Deferred items in the review record do not exist merely because SPEC describes them.

## Invariants

- Keep reference preservation, declared interpretation, model intent, check outcomes and human decisions distinct.
- Observe actual submitted circuits/counts; a separately reconstructed circuit is not execution evidence.
- Unsupported, inconclusive and failed paths remain explicit. A matching circuit or a hash is not scientific certification.
- Keep exact evidence immutable; review decisions bind its digest and do not change machine outcomes.
- Execute inspected code locally only after explicit trust. Environments/subprocesses are not a hostile-code sandbox.
- Use one Python toolchain and free static hosting. No new paid services, public Python uploads, model keys in the browser or silent recorded fallback.
- Freeze contracts before parallel edits. Run consolidated checks after shared edit waves and exercise actual CLI/browser paths before delivery.

## History and communication

`archive/research-2026-10/` contains superseded research/proposals. It is not an instruction source or active task queue. The old Ledger implementation issues are superseded; do not revive them.

The user reports one research email sent with no reply. Additional outreach requires new authorization. For third-party copy, read Humanizer and ASD-STE100; use plain titles and spaced paragraphs. Never invent reviewers, user adoption, human acceptance, benchmark rates, deployment or contest odds.

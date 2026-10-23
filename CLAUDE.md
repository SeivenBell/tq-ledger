# tq-ledger

Severyn Balaniuk's Build North 2026 hackathon project (submission Oct 25, 2026, 11:59 PM ET).

**Conditional recommendation: Q-Day Ledger**, a source-linked comparison/refusal workbench for public quantum cryptanalysis claims. This is planning, not an implemented app. Severyn's final choice remains open on issue #14 ("Choose the project to build"); do not start product implementation until that choice is recorded.

## Start here

- `docs/BRIEFING-2026-10-24.md`: the state of everything and the plan.
- `CONTEXT.md`: domain vocabulary. Use these terms exactly.
- `docs/build/PRODUCT.md`, `docs/build/ARCHITECTURE.md`, `docs/build/PLAN.md`: what to build, how, and in what order.
- Implementation tickets: GitHub issues labelled `build` (T1 to T12 plus human review T1b). Read PLAN before starting a ticket; it distinguishes core from deferred extensions. Old issue comments are historical.

## Rules for coding agents

- Work one ticket at a time; touch only the files it names; open a PR linked to the issue.
- Never invent a number or copy a research quote as certified data. Re-anchor candidate evidence from `docs/research/build/claims-classic.md` and `claims-2026.md` to pinned canonical source text.
- Never convert logical resources to physical ones; never add attack circuits or physical-estimation features. Strict spans establish provenance, not scientific truth; categorical semantics need human review.
- `make test` and `make verify` are required acceptance interfaces for the future build, not currently implemented commands. Once implemented, exercise the actual UI/CLI changed path before delivery.

## Research

Planning ran as a Wayfinder map (issue labelled `wayfinder:map`). Research reports live in `docs/research/`; research tickets follow `docs/wayfinder/research-brief.md`.

# tq-ledger

Severyn Balaniuk's Build North 2026 hackathon project (submission Oct 25, 2026, 11:59 PM ET).

**Recommended build: Q-Day Ledger**, cited and comparable cards for quantum cryptanalysis cost claims. Severyn confirms the pick on issue #14 ("Choose the project to build").

## Start here

- `docs/BRIEFING-2026-10-24.md`: the state of everything and the plan.
- `CONTEXT.md`: domain vocabulary. Use these terms exactly.
- `docs/build/PRODUCT.md`, `docs/build/ARCHITECTURE.md`, `docs/build/PLAN.md`: what to build, how, and in what order.
- Implementation tickets: GitHub issues labelled `build` (T1 to T12). Each ticket names the files it may touch and its acceptance tests.

## Rules for coding agents

- Work one ticket at a time; touch only the files it names; open a PR linked to the issue.
- Never invent a number. Card data comes verbatim from `docs/research/build/claims-classic.md` and `claims-2026.md`.
- Never convert logical resources to physical ones; never add circuit or attack-estimation features.
- Run `make test` and `make verify` before opening a PR.

## Research

Planning ran as a Wayfinder map (issue labelled `wayfinder:map`). Research reports live in `docs/research/`; research tickets follow `docs/wayfinder/research-brief.md`.

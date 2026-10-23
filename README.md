# Build North research

Project selection is still open. The previous Q-Day Ledger recommendation has been withdrawn. The [current decision memo](docs/decision/ranked-memo.md) compares four concrete alternatives and explains the provisional preference for a small quantum-code upgrade reviewer. No main application is built or deployed.

Start here:

- [Which project should we build?](docs/decision/ranked-memo.md) — recommendation, alternatives, usefulness, build limits and reasons to stop.
- [What we actually ran](docs/research/round2/workflow-checks.md) — a real Sonnet/Qiskit migration, plus limited scientific-trace and battery-data checks.
- [Current status and next steps](docs/BRIEFING-2026-10-24.md) — accounts, dated event information and the remaining human decision.

The four new investigations cover [quantum upgrades](docs/research/round2/quantum-workflows.md), [claim-review workflows](docs/research/round2/claim-workflows.md), [scientific reproduction](docs/research/round2/scientific-reproduction.md) and [research data/operations](docs/research/round2/scientific-operations.md). Each records source dates and reading depth.

Both original Fable reports are now preserved: [practitioner problems](docs/research/originals/practitioner-pain-fable.md) and [circuit discovery](docs/research/originals/ai-circuit-discovery-fable.md). Their full texts were supplied in chat; their original commits and reported experiments are not independently verified.

The real notebook experiment is reproducible from [its separate research branch](https://github.com/SeivenBell/tq-ledger/tree/research/round2-qaoa-probe/prototypes/round2-qaoa). The older [QRef probe](prototypes/qref-probe/README.md) uses deliberately planted failures; neither probe is a production verifier.

Files in `docs/build/` and the Ledger vocabulary in `CONTEXT.md` are archived proposals, not an active build queue. [Severyn chooses the project](https://github.com/SeivenBell/tq-ledger/issues/14) before implementation. Outreach is paused; no practitioner inquiry has been sent.

Repository code is Apache-2.0. Cited sources and copied original reports retain their applicable rights and terms; a research quote is not a certified scientific claim.

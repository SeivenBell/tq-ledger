# QRef

**Review a quantum-code migration before relying on it.**

Status: **release 0.1 — owner-approved core slice, implemented.** Live report: **https://seivenbell.github.io/tq-ledger/**. [All examples](https://seivenbell.github.io/tq-ledger/examples.html): fresh Claude port, earlier research port and a labelled seeded regression. Guided demo: `scripts/demo.sh`. Deferred work (ZIP export, full fixture matrix, Linux reproduction) is listed in the [review record](docs/reviews/external-review.md).

## Run it

```bash
uv sync --frozen
uv venv --python 3.11.12 .qref/envs/reference
uv pip install --python .qref/envs/reference/bin/python -r evidence/qaoa/legacy-requirements.txt
uv venv --python 3.11.12 .qref/envs/target
uv pip install --python .qref/envs/target/bin/python -r evidence/qaoa/modern-requirements.txt

uv run qref propose --case cases/qaoa.json --out runs/proposal    # existing Claude subscription; never executes code
# inspect runs/proposal/target.py before the next step
uv run qref run --case runs/proposal/case.json \
  --reference-python .qref/envs/reference/bin/python \
  --target-python .qref/envs/target/bin/python \
  --out runs/run --trust-local-code                                # exit 0 consistent, 1 differences, 2 incomplete/invalid
open runs/run/index.html
uv run qref verify-bundle --run runs/run
uv run pytest
```

`--trust-local-code` is required because candidate Python runs with your local permissions. Environments isolate versions, not hostile code.

## Start here

- **[Complete specification](SPEC.md):** what to build, supported workflow, exact proposed commands/contracts, scientific limits, security, UI and free deployment.
- **[Independent review prompt](REVIEW.md):** copy this to the next AI. Review first; do not begin coding in the same invocation.
- **[Implementation plan](PLAN.md):** contract gate, ownership, parallel work, acceptance and release sequence.
- [Product context](PRODUCT.md) and [domain language](CONTEXT.md).
- [Proposed report design](docs/design/report-brief.md), [readable layout schematic](docs/design/report-layout.png) and [SVG source](docs/design/report-layout.svg).
- [Planning proof and limits](docs/reviews/planning-verification.md).

## The complete workflow we propose

A local model proposes a port. A developer inspects it before execution. Two pinned environments run the reference and target; independent checks inspect the actual submitted circuits, classical interpretation and sampling settings. A portable report shows observations, model intent, human decisions and unchecked scope separately.

The public copy is a static report on free GitHub Pages—not a hosted Python executor or live-model website. No new paid services are assumed.

## What runs now

`qref propose`, `qref run`, `qref report` and `qref verify-bundle` are in `src/qref/`. `cases/qaoa.json` runs the [retained seed](evidence/qaoa/README.md) research port. `examples/` holds the curated, verified exports that are published to Pages.

These results do not establish general reliability, a rate of hidden agent errors, a customer, or scientific certification. Checks cover only the declared inputs.

## Historical material

All abandoned Ledger plans, competing-project research, both complete original Fable reports, the old planted-error prototype and cloud launcher are preserved under **[archive/research-2026-10](archive/research-2026-10/README.md)**. Do not build from that directory. No active compatibility stubs remain at old paths.

One research inquiry was sent with no reply. Additional outreach is not authorized. Do not interpret that email as migration-user validation.

Repository code is Apache-2.0. Copied source and dependencies keep their own licences. Preserve the included Qiskit attribution, and disclose MQT QCEC as the checking engine.

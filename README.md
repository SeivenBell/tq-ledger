# QRef

**Review a quantum-code migration before relying on it.**

Status: review-ready specification and executable research evidence. The product CLI, report interface and public deployment are not implemented yet. The user authorized planning and repository cleanup; implementation follows independent review and separate approval.

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

## What can run now

[The retained QAOA seed](evidence/qaoa/README.md) contains the original licensed helper code, real model port and observations. It is research code, not the future QRef command suite. The newer [planning probe](https://github.com/SeivenBell/tq-ledger/tree/67db6c595927faa91a85f64a7d1845f1c89b09dc/prototypes/qref-spec-probes) proves the subscription-only proposal route, actual Aer submission capture and independent same-count decoding on the seed. It is deliberately kept off main as throwaway code.

These probes do not establish general reliability, a hidden-agent-error rate, a customer or scientific certification. The actual product must satisfy the specification's failure/coverage/export/browser criteria.

## Historical material

All abandoned Ledger plans, competing-project research, both complete original Fable reports, the old planted-error prototype and cloud launcher are preserved under **[archive/research-2026-10](archive/research-2026-10/README.md)**. Do not build from that directory. No active compatibility stubs remain at old paths.

One research inquiry was sent with no reply. Additional outreach is not authorized. Do not interpret that email as migration-user validation.

Repository code is Apache-2.0. Copied source and dependencies retain their applicable licences; preserve the included Qiskit attribution and disclose MQT QCEC as the checking engine. No live URL or finished submission is claimed by this README.

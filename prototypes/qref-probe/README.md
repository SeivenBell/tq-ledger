# QRef probe (backup option, not the main build)

A feasibility probe written on 2026-10-23 for the backup project: a behavioural referee that checks whether a Qiskit program ported by a coding agent (Qiskit 0.46 to 2.x) still behaves like the original.

- `qref/trace.py`: runs any script unmodified and records every simulated circuit (exact distributions for static circuits, seeded 20,000-shot counts otherwise, operation mix), for both Qiskit versions.
- `qref/compare.py`: the referee. Tier 1 compares circuit behaviour (exact total variation distance, or a chi-square test with a Bonferroni correction); tier 2 compares replayed printed outputs. Exit code 0 = pass, 1 = fail.
- `cases/`: three legacy scripts, their ports, seeded bugs (`mut_*`), and equivalent rewrites (`ok_*`).
- `./run_all.sh` builds both environments with `uv` if missing and runs everything (about 20 seconds once installed).

Result: 11 comparisons agreed with their expected verdicts (6 pass, 5 deliberately seeded failures), including a planted parameter-binding bug that made QAOA look better. This is a feasibility demonstration, not a measured real-world migration error rate. Full report: `../../docs/research/build/qref-probe.md`.

Run only trusted local scripts. The tracer executes Python in-process; it is not a sandbox or a safe public upload endpoint. Dynamic-circuit sampling can miss small effects, and unhooked APIs are outside this probe's coverage.

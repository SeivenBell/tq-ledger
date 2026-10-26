# QRef feasibility probe: behavioural referee for agent-made Qiskit migrations

**Verdict:** the referee core is very buildable (**buildability 5/5**). As a hackathon demo it is believable but narrow (**demo credibility 3/5**). The Claim Ledger is still the better primary. Keep QRef as the backup.

On 3 legacy scripts and 11 port/variant comparisons, the referee agreed with all expected verdicts: 6 correct variants passed and 5 deliberately seeded failures were caught. One planted parameter-binding bug makes the ported QAOA appear better. The integration rerun of `./run_all.sh` confirmed these counts; the earlier “13 of 13” total was a counting error. No unseeded agent-migration error rate was measured.

## What I built (all in `/tmp/qref-probe`)

| Path | What it does |
|---|---|
| `legacy/` | uv venv: Python 3.11, qiskit 0.46.3, qiskit-aer 0.14.2, qiskit-algorithms 0.3.1 (numpy 2.4.6 worked) |
| `modern/` | uv venv: Python 3.13, qiskit 2.6.1, qiskit-aer 0.18.0 |
| `cases/s{1,2,3}_*/legacy.py`, `port*.py`, `mut_*.py`, `ok_*.py` | The scripts, ports and variants |
| `qref/trace.py` (~190 lines) | Tracer that runs any script unmodified via `runpy` and works with both Qiskit versions |
| `qref/compare.py` (~140 lines) | The referee: exit code 0 = PASS, 1 = FAIL |
| `run_all.sh` | Rebuilds both envs if missing, traces every script twice (normal and `--replay`), compares. Full run takes about 20 s. |
| `traces/*.json` | Trace output |

**What the tracer does**
- It hooks `qiskit_aer...AerBackend.run`. That one hook covers `execute()`, `QuantumInstance.execute`, and `backend.run` in both versions.
- It also hooks `StatevectorSampler.run` (SamplerV2). It expands each parameter sweep the way the primitive does: values bound by position, in `circuit.parameters` order.
- For every bound circuit it records:
  - the exact distribution over classical bits, from a Statevector, when the circuit is "static" (all measurements at the end, no `c_if`/`if_test`/reset);
  - a 20,000-shot run on a fresh `AerSimulator` with a fixed seed, for every circuit;
  - the mix of operations in the circuit.
- With `--replay`, sampled results are replaced by deterministic "ideal counts" (exact probabilities rounded so they sum to the shot count). This uses `Result` data on the Aer path and `Statevector.sample_memory` on the Sampler path. Legacy and ported code then post-process identical data, so their printed outputs can be compared.

**How the referee judges**
- **Tier 1, circuit behaviour.** Circuits are paired in the order they were submitted.
  - Both static: exact total variation distance (TVD); FAIL if it is above 1e-9.
  - Otherwise: chi-square homogeneity test on the 20k-shot counts; FAIL only if p < 1e-3/m (Bonferroni) **and** TVD > 0.02.
  - It also tries to match a failing port circuit to a different legacy circuit, to spot permutations.
- **Tier 2, printed outputs.** The numbers in the replayed stdout must match to 1e-9 when every circuit was replayable. Otherwise this tier is only advisory.

## Scripts and ports

| Case | Legacy APIs used | Port | Bug |
|---|---|---|---|
| s1 GHZ + biased Bell | `qiskit.execute`, `Aer.get_backend("qasm_simulator")`, `cnot` | `AerSimulator` + `transpile` + `run`, `cx`, `u` | none |
| s2 QAOA MaxCut grid search (4 nodes, asymmetric graph, 30 grid points) | `Parameter`, `bind_parameters({gamma:…, beta:…})`, `execute` | `StatevectorSampler` with a parameter sweep | **deliberate:** sweep columns are `(gamma, beta)`, but SamplerV2 binds by position in `qc.parameters` order, which is alphabetical `(beta, gamma)` |
| s3 teleportation | `c_if`, `QuantumInstance` | `if_test` + `AerSimulator` | none |

The s2 bug is silent and looks like an improvement: the port reports a *higher* best expected cut (2.6572 against legacy's 2.355). That happens because it is actually evaluating points outside the legacy grid.

## Results (`./run_all.sh`, all observed)

| Case / variant | Expected | Referee | Evidence |
|---|---|---|---|
| s1 port | pass | **PASS** | 2/2 circuits equivalent; replayed outputs match |
| s1 `mut_postproc_endian` (`bits[0]` instead of `bits[-1]`) | fail | **FAIL** | Tier 1 passes 2/2 (circuits identical). Tier 2 catches it: `P(q0=1) 0.25` became `1.0` |
| s1 `mut_measure_map` (measure `[0,1,2]→[2,1,0]`) | fail | **FAIL** | circuit 1 exact TVD = 0.75 |
| s1 `ok_other_seed` | pass | **PASS** | |
| **s2 port (deliberate bug)** | fail | **FAIL** | 28/30 circuits differ (TVD up to 0.21). Replayed output: `best gamma 0.1 beta 1.1281` became `best gamma 1.2766 beta 0.4427`; best cut `2.3467` became `2.6367` |
| s2 `port_fixed` (binding in `qc.parameters` order) | pass | **PASS** | 30/30 equivalent; outputs match |
| s2 `mut_rx_halfangle` (`rx(beta)` instead of `rx(2*beta)`) | fail | **FAIL** | 0/30 equivalent |
| s3 port | pass | **PASS** | sampled tier; operation mix changed from `x,z` (`c_if`) to `if_else` (noted only) |
| s3 `mut_swapped_corrections` (if-tests on the wrong registers) | fail | **FAIL** | sampled TVD = 0.152, chi-square p ≈ 0 |
| s3 `ok_deferred_measurement` (feed-forward replaced by `cx`/`cz` before measurement) | pass | **PASS** | different circuit and different samples: TVD = 0.0086, p = 0.68. The transpiler dropped the `cz` as a diagonal gate before measurement, which is still correct |
| s3 `ok_other_seed` | pass | **PASS** | |

Two observations from these runs:
- **Without replay, comparing raw outputs would have given a false alarm on the *correct* s2 port.** Legacy reported `gamma 3.0416, beta 0.4427` and the fixed port `gamma 0.1, beta 1.1281`. These are points related by QAOA's (γ,β)→(π−γ, π/2−β) symmetry, with the tie broken by shot noise. With replay, both print identical output.
- **The same Aer seed gave bit-identical counts on aer 0.14.2 and aer 0.18.0** (for example GHZ `{'000': 2020, '111': 2076}` in both).

## Effort

- **Wall clock:** about 7 minutes of agent time from the first command to the final run, timed by the Python kernel clock. That excludes about a minute lost when the bash tool would not start; I ran every command through Python `subprocess` instead.
- **Size:** 543 lines in total across the tracer, referee, legacy scripts and ports (ports include variants).
- **Disk:** `legacy` 254 MB, `modern` 158 MB.
- [INFERENCE] A human doing the same thing would need roughly 2–4 hours, mostly spent fighting the legacy environment.

## What broke (environment pitfalls)

1. **`QuantumCircuit.u3` is already removed in qiskit 0.46.3** (`AttributeError: ... no attribute 'u3'`). So "legacy" tutorial code partly does not run even on the last 0.x release. I rewrote that line as `u`; `cnot` still works.
2. **qiskit-aer 0.13.3 with terra 0.46.3 fails to transpile a batched `execute([ghz, biased], …)`.** The error was `TranspilerError: Unable to translate ... to the backend's target basis: ['measure','snapshot','cx','h','barrier']`. It looks like the target basis was taken from the first circuit. This happened with `qasm_simulator`, `aer_simulator` and `aer_simulator_statevector`. **Fix: pin qiskit-aer 0.14.2.**
3. qiskit 0.46.3 imported and ran on numpy 2.4.6 without problems (I expected this to break).
4. macOS `/bin/bash` 3.2 has no associative arrays, so `run_all.sh` uses a `case` function instead.
5. Not tested: `qiskit.algorithms` VQE with `QuantumInstance`, and `opflow`. Each legacy idiom needs its own hook.

## How far this generalizes beyond toy scripts

**Holds up**
- Hooking the execution boundary needs no changes to the scripts.
- Exact equivalence on static circuits works up to about 25 qubits.
- The statistical tier with a minimum effect size worked for feed-forward circuits.
- Deterministic replay is what makes post-processing bugs (bit order, argmax) detectable. The circuit tier alone missed the endianness bug.

**Breaks or needs work** (all [INFERENCE] except where noted)
- Pairing circuits by submission order is fragile. It breaks if a port batches or reorders circuits, or uses optimizer loops whose path diverges. Replay helps with determinism, but VQE/COBYLA paths can still diverge after a small numeric difference.
- Not hooked:
  - Estimator primitives (expectation values);
  - `qiskit-ibm-runtime`;
  - noise models;
  - layout and routing on real devices: the hardware-transpile output must be compared as a logical circuit, which needs the layout handled.
- The statistical tier misses effects with TVD under 0.02, such as small angle errors in feed-forward circuits.
- Tier 2 depends on the port keeping the same print format.
- Reproducing old environments (point 2 above) costs more than the referee logic itself.

**Prior art**
- *Qiskit Code Migration with LLMs* (arXiv 2606.20173, 2026-06-18; I read the abstract only) evaluates hallucination and descriptive quality.
- *quantum-api-drift* (arXiv 2607.04072, 2026-07-05; abstract plus partial README) defines "version fidelity" as **execution success**. Its sample tests are `assert result is not None`.
- I found no tool that checks behavioural equivalence of migrations. I only did one search, so this is weak evidence that the idea is new, not proof.

## Feasibility versus the Claim Ledger

| | QRef | Claim Ledger |
|---|---|---|
| Buildability in about 12 h | **5/5**: the core is done; the remaining work is a UI, an LLM porting agent, the Estimator hook, and about 10 cases | [INFERENCE] about 4/5: more moving parts (extraction, span checks, comparison gates, UI) |
| Demo credibility | **3/5**: the "agent made a plausible migration that silently got better results and the referee caught it" moment is strong and live. But it is clearly toy scale, it is a terminal tool unless I add a UI, and the audience is narrow (Qiskit maintainers and quantum software teams) | [INFERENCE] higher: post-quantum risk feeds CISO budgets and decisions, which better fits Georgian investors and the Real-World Impact criterion |
| Innovation evidence | Abstract-level leads only; insufficient to establish novelty | per the other research reports |
| Partner prizes | none apply naturally | SurrealDB (agent memory) could plausibly apply |

[INFERENCE] QRef fits the verification theme and already has a runnable small-circuit core. Keep it as a separate backup; do not dilute the Ledger demo with a second product. The remaining usability, generalization and real migration-error evidence is not demonstrated by the planted cases.

**Commands:** `cd /tmp/qref-probe && ./run_all.sh`. Single comparison: `modern/bin/python qref/compare.py traces/s2_qaoa.legacy.json traces/s2_qaoa.port.json traces/s2_qaoa.legacy.replay.json traces/s2_qaoa.port.replay.json`.
# What we actually ran

Research date: October 23, 2026. These are small deciding experiments, not product benchmarks or a finished app.

## Bottom line

A real Qiskit notebook gave us a useful review example: the migrated circuits agree, but the sampling setting changes. The coding agent had already disclosed the change. An execution report can confirm its explanation; this experiment does not show that our proposed tool catches mistakes a normal agent misses.

The adjacent checks also argue against unnecessary products. A released scientific benchmark already grades the numerical failure we inspected. A requested battery calculation reduces to simple arithmetic, although integrating it correctly still requires domain rules.

## 1. Qiskit notebook upgrade

### Input and method

We used the archived Qiskit textbook's [QAOA notebook at commit `0ae9050`](https://github.com/qiskit-community/qiskit-textbook/blob/0ae905083ec3872d7ddc6bb4001d5468f476d93f/content/ch-applications/qaoa.ipynb). Read depth: partial notebook, all code cells inspected in the source investigation; the actual execution used the helper functions in cell 18. The root Apache-2.0 licence was read in full. The notebook is deliberately old, not evidence of a current maintainer request.

The source helpers were not repaired before the comparison. A single offline Claude Sonnet 5.5 attempt produced the port and explanatory notes. It had file tools but no execution or web tools. There was no feedback or repair round. Its prompt, output, exact dependencies, observer scripts and recorded results are preserved on the separate [experiment branch](https://github.com/SeivenBell/tq-ledger/tree/research/round2-qaoa-probe/prototypes/round2-qaoa), commit `6233ef3`.

| Runtime | Python | Qiskit | Aer | NumPy | QCEC |
|---|---|---|---|---|---|
| Source | 3.11.12 | 0.46.3 | 0.14.2 | 1.26.4 | Not used |
| Target | 3.11.12 | 2.6.1 | 0.18.0 | 2.4.6 | 3.11.0 |

The input grid contained three small graphs and three angle lists, covering one and two QAOA layers. Each case requested 512 and 17 shots. A shot is one simulated measurement. We recorded actual completed shots, output probabilities and the decoded MaxCut objective.

MQT QCEC checked the corresponding bound circuits. Exact statevector probabilities supplied a separate numerical comparison on these small noiseless inputs. These checks answer different questions: circuit equivalence is stronger than matching one output distribution, but neither proves that the surrounding Python program behaves identically.

### Observed results

| Check | Observed result | What it establishes |
|---|---|---|
| Unchanged source imported in the target runtime | `ImportError`: `qiskit.Aer` unavailable | A genuine API break, not a planted defect |
| Nine circuit/parameter pairs | All QCEC verdicts `EquivalenceCriterion.equivalent` | Circuit agreement on the checked bound cases |
| Exact output probabilities | Largest absolute difference `1.5265566588595902e-16` | Numerical agreement within floating-point precision |
| Exact decoded objectives | Largest absolute difference `8.881784197001252e-16` | Agreement for the declared graph/angle cases |
| Source calls requesting 512 or 17 shots | Always 1,024 completed shots | The historical helper did not honor the requested setting in this runtime |
| Port calls requesting 512 or 17 shots | Completed 512 or 17 respectively | The port honors the requested setting |

This is one behavior change observed across 18 executions per runtime, not 18 distinct bugs. The old helper assigns `backend.shots` and passes `nshots=512`. The port supplies `shots=shots` to the actual run call.

**The model disclosed that change before execution.** Its notes identified the old setting as probably ineffective and said the port would honor the caller's argument. Calling this a silent agent error would misrepresent the experiment. The old behavior may be the bug; preserving it is not automatically the correct scientific choice. A reviewer must decide whether to preserve the old experiment or accept the correction.

The CLI reported 34.76 seconds and an estimated $0.0818034 for the model call. That estimate is not an invoice, an API-credit debit or the total research/build cost.

### Setup failures and limits

The proposed shared NumPy 1.26.4 pin was incompatible with Qiskit 2.6.1, which requires NumPy 2. We installed separate environments instead. Legacy QASM import also failed on `rzz` until the importer used Qiskit's documented `LEGACY_CUSTOM_INSTRUCTIONS`. Neither setup failure was treated as a circuit mismatch.

The observation harness was written after the port. Its graph and angle grid came from the preceding research plan, but this was not a blinded or preregistered evaluation. We did not run the full notebook, optimizer, plotting cells, hardware, noise models, dynamic control or a second independent migration. We measured no agent error rate, reviewer time saving or willingness to adopt the report.

The earlier [QRef probe](../build/qref-probe.md) used planted failures. This new example does not replace that test with a claim about naturally occurring failures. It adds a real API migration and an independently observed setting change.

**Decision implication [INFERENCE]:** a narrow upgrade-review report is technically credible. Its incremental benefit over a normal coding agent plus existing QCEC/Aer checks remains unproven. Prefer an example or integration for existing tools unless a reviewer identifies a recurring task.

## 2. A scientific agent's completed run with a failed answer

We inspected the released [ReplicationBench `ls_cal` trace](https://raw.githubusercontent.com/Christine8888/replicationbench-release/main/logs/text-format/gpt5-base-1/ls_cal.out) and its [complete `cold_sparam` task JSON](https://raw.githubusercontent.com/Christine8888/replicationbench-release/main/src/dataset/tasks/ls_cal/cold_sparam.json). Read depth: partial trace—instructions, relevant implementation, final executed output, submission and score; full task JSON. These are released 2025 artifacts, not a measurement of current frontier-model performance.

A throwaway Python check extracted the recorded numerical answer and applied the task's existing absolute tolerance:

| Field | Value |
|---|---:|
| Recorded numerical answer | 0.001223001128203661 |
| Benchmark reference | -0.00319 |
| Absolute tolerance | 0.001 |
| Absolute difference | 0.004413001128203661 |
| Within tolerance | No |

The trace ends with “Task completed,” but the numerical answer is outside the benchmark tolerance. The benchmark's own scoring already captures this failure. Its overall score covers five tasks; this check does not establish that the entire paper failed.

We did not rerun the experiment or read the original calibration paper deeply enough to endorse the physical reference. The trace implements the requested port swap, so we cannot blame its omission. The cause of the numerical discrepancy remains undiagnosed.

Trace bytes: SHA-256 `955f2c3430e144044dfa5f83134c690bfb51c5cd0e04a238b2174e946f806f97`.

**Decision implication [INFERENCE]:** linking answers to execution evidence can help review. A new report that merely repeats this existing grade does not establish an unmet need. CODECHECK or benchmark maintainers would need to identify the missing review step.

## 3. Battery-data calculation

We parsed the header and selected rows of the public [SINTEF BDF CSV](https://raw.githubusercontent.com/battery-data-alliance/battery-data-format/main/data/SINTEF__LiGrR2032__2024-04-30__25degC__Landt.csv). Read depth: partial—preamble/header and selected resting/discharge rows, not a scientific audit of the whole file. A throwaway Decimal calculation applied `power = current × voltage`.

| Parsed data row | Current, A | Voltage, V | Calculated power, W |
|---|---:|---:|---:|
| 1 | 0.0000 | 2.9215 | 0.00000000 |
| 2882 | -0.0002 | 2.6450 | -0.00052900 |
| 2883 | -0.0002 | 2.6280 | -0.00052560 |

Input bytes: SHA-256 `10867f1143704420e9e82a49f22c7661cebc62658bd33402bdde4f8190326c36`.

This is arithmetic on real input, not a tested BDF contribution. We did not validate capacity/energy integration, signs across instrument formats, timestamps, missing-value rules or package compatibility. Data-specific redistribution rights were not established, so the CSV is linked rather than bundled.

**Decision implication [INFERENCE]:** the [explicit request for calculated columns](https://github.com/battery-data-alliance/battery-data-format/issues/136) is stronger demand evidence than our speculative app ideas. Its body and comments were read in full in [the operations report](scientific-operations.md). The useful deliverable is likely a small upstream function with clear rules, not an AI platform.

## Evidence status

Only the QAOA helper workflow was executed end to end across two runtimes. The scientific trace was checked without rerunning its experiment. The battery check exercised arithmetic, not the package feature. No main app, hosted reviewer, customer trial or universal certification was built.

No practitioner inquiry was sent. Outreach remains paused at the user's request.

# A real notebook upgrade experiment

This is a research probe, not a production checker or the final hackathon app.

Question: can a small execution report reveal a behavior change that circuit comparison alone does not cover?

## Input and result

The source is the Apache-2.0 [Qiskit textbook QAOA notebook](https://github.com/qiskit-community/qiskit-textbook/blob/0ae905083ec3872d7ddc6bb4001d5468f476d93f/content/ch-applications/qaoa.ipynb). The original notebook and licence are included. `legacy_functions.py` contains its unchanged helper cell, with the required imports added. Attribution remains with the Qiskit textbook contributors.

One offline Claude Sonnet 5.5 attempt produced `port_functions.py` and `port-notes.md`. It had file tools but no execution or search tools. The researcher then ran both versions independently.

- Unchanged source does not import under Qiskit2.6.1 because `qiskit.Aer` was removed.
- All nine checked circuit/parameter cases are equivalent according to MQT QCEC3.11.0. Exact output probabilities and objective values agree within floating-point precision.
- The source actually uses1,024 shots when callers request512 or17. The port uses the requested512 or17.
- This is one sampling-setting change observed across18 executions per runtime, not18 independent bugs.
- The model already disclosed the intended change and its uncertainty. The report confirms its claim by execution. It does not demonstrate a hidden agent error or superiority over a normal coding agent.

A shot is one simulated measurement. Changing the shot count changes sampling uncertainty even when the circuit is equivalent. The old program is a reference for preservation, not proof that its behavior is scientifically preferable.

## Run

From this directory, with `uv` installed:

```bash
uv venv --python 3.11.12 legacy
uv pip install --python legacy/bin/python -r legacy-requirements.txt
uv venv --python 3.11.12 modern
uv pip install --python modern/bin/python -r modern-requirements.txt
legacy/bin/python observe_functions.py legacy_functions.py legacy-observations.json
modern/bin/python observe_functions.py port_functions.py modern-observations.json
modern/bin/python compare_observations.py
```

`comparison.json` contains the circuit verdicts and actual shot counts. The recorded input grids cover three small graphs and three angle settings. The source four-cycle is one graph; the additional four- and five-node graphs are declared probe inputs. They are not hidden author tests.

The observation script was written after the port. The inputs came from the prior research plan, but this was not a blinded, preregistered benchmark. The optimizer, plotting cells, hardware and dynamic circuits were not exercised. No defect was planted.

## Setup facts

The proposed shared NumPy1.26.4 pin failed: Qiskit2.6.1 requires NumPy2. The isolated target therefore uses NumPy2.4.6. The legacy side uses1.26.4. Exact resolved dependencies are in the two requirement files.

Importing the legacy QASM output also required Qiskit's documented `LEGACY_CUSTOM_INSTRUCTIONS` for `rzz`. Without that importer setting, the comparison failed before QCEC ran.

`baseline-run.json` records the actual resolved model, prompt, usage and CLI cost estimate. Its approximately$0.082 estimate and34.76-second duration describe that one model call, not a build cost or an invoice. Agent notes are preserved as model output, not treated as independently verified statements.

Run only these inspected local scripts. This probe does not sandbox arbitrary Python input. Environment directories and caches are not committed.

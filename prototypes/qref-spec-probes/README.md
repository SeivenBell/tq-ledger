# QRef planning probes

Throwaway research code, not the QRef implementation.

## Questions answered

1. Can the installed Claude Code CLI use the existing subscription to return a structured port with no model tools?
2. Can one scoped Aer hook capture the actual submitted circuit in both pinned runtimes, without depending on a closure variable name?
3. Can the returned objective be checked against independent decoding of the same captured counts?

## Observed answers

Yes, for this inspected QAOA helper case.

- Claude Code 2.1.308 used the existing claude.ai Pro login. The tested invocation returned valid structured output with code, summary, intended changes and uncertainties. It used the flags recorded in `proposal-record.json`, not `--bare`.
- The resolved model was `claude-sonnet-5-5`. One CLI invocation took about 21 seconds and used two SDK turns. The approximately $0.045 client estimate is not an invoice or an API-credit debit.
- The model disclosed the intended shot correction before execution. Its original uncertainty about direct Aer submission is preserved in the record rather than rewritten after the successful run.
- After inspection, the reference and generated target each completed 18 executions through the `AerBackend.run` class hook.
- Each side's classical helpers agreed with an independently written negative-cut rule on 64 basis assignments across the three graphs. Returned objectives agreed with independent decoding of each execution's actual histogram.
- Actual terminal measurement maps were identity maps. Nine distinct actual submitted circuit pairs were QCEC-equivalent, covering the 18 execution pairs. Ideal output probabilities agreed within the probe's 1e-10 tolerance.
- The reference completed 1,024 shots; the target completed the requested 512 or 17.

These are positive capability checks, not a blinded benchmark, an error rate, a complete protocol test or a claim of product novelty. The prompt explicitly described the previously observed shot behavior. No hidden model mistake was discovered.

## Run

Inspect the source before executing it. This does not sandbox Python.

With Python 3.11.12 and `uv` available, from this directory:

```bash
uv venv --python 3.11.12 legacy
uv pip install --python legacy/bin/python -r legacy-requirements.txt
uv venv --python 3.11.12 modern
uv pip install --python modern/bin/python -r modern-requirements.txt
legacy/bin/python capture_probe.py reference.py reference-captured.json
modern/bin/python capture_probe.py generated_target.py target-captured.json
modern/bin/python compare_probe.py reference-captured.json target-captured.json capture-comparison.json
```

The results checked into this branch are the recorded run. Re-execution may produce different sampled values. It must not be called a reproduction of exact random streams across library versions.

`proposal-record.json` preserves the actual prompt, schema, fixed argv, timestamps, resolved model metadata and structured answer. Repeating that model request is optional and not required to check the recorded port. Do not use `--bare` with this subscription workflow: official documentation states that bare mode omits OAuth/keychain authentication.

## Deliberate limits

The capture probe imports the inspected module before installing the hook. It therefore does not prove production interception of import-time execution. It uses assertions and has no full status/error protocol, no schema/manifest implementation, no publication/export UI, no timeout handling and no general unsupported-input support. Those belong to the reviewed implementation specification, not this probe.

Only four- and five-qubit seed inputs were exercised in the capture probe. The complete proposed eight-qubit scope, negative workflow fixtures, missing data, partial workers, safe HTML exports and fresh Linux provisioning were not tested. The focused follow-ups below cover only the named phase, QPY and authentication cases—not the remaining QCEC branches or the production protocol.

The reference is the Apache-2.0 Qiskit textbook helper cell from [snapshot 0ae9050](https://github.com/qiskit-community/qiskit-textbook/blob/0ae905083ec3872d7ddc6bb4001d5468f476d93f/content/ch-applications/qaoa.ipynb), with imports added. Attribution remains with the Qiskit textbook contributors; the licence is included. The target is the real model-generated port recorded here. Qiskit/Aer and MQT QCEC supply the quantum execution/checking capabilities.

## Follow-up: challenge the phase mapping

`phase_probe.py` and `phase-results.json` preserve a direct run in the same pinned modern environment. Identical circuits returned `equivalent`; a gate-level global minus sign returned `equivalent_up_to_global_phase`; a relative Z change returned `not_equivalent`. Setting only Qiskit's global-phase metadata returned `equivalent`, so this import path does not demonstrate preservation of that metadata.

The v3.11.0 [Python binding docstrings](https://github.com/munich-quantum-toolkit/qcec/blob/v3.11.0/bindings/register_equivalence_criterion.cpp) reverse the two phase descriptions. The [alternating-checker implementation](https://github.com/munich-quantum-toolkit/qcec/blob/v3.11.0/src/checker/dd/DDAlternatingChecker.cpp) explicitly emits `EquivalentUpToGlobalPhase` for a non-one global weight on the identity. An internal reviewer recommended swapping the mapping based on the docstrings; source and runtime counter-evidence reject that recommendation. This does not exercise `equivalent_up_to_phase`, probable outcomes or deadlines.

Run with `modern/bin/python phase_probe.py`. The successful original invocation executed the identical source through `python -c`; an initial invocation without an explicit accessible cwd failed at import because of workstation permissions.

## Follow-up: native snapshots and clean authentication

`qpy_probe.py` created a two-qubit measured circuit with nonzero global phase, dumped/loaded it **within each runtime**, and confirmed circuit/global-phase equality. `qpy-roundtrip.json` records Qiskit 0.46.3 and 2.6.1 outcomes. This supports opaque native snapshot retention; it does not prove cross-version loading or capture-before-submission integration. Run with each environment's interpreter.

`auth-preflight.json` contains only the categories returned by `claude auth status` from an accessible temporary cwd with the proposed environment allowlist. It returned logged-in `claude.ai`, `firstParty`, exit 0; no model request was made by this follow-up. Account details, secrets and environment values were not published. The earlier successful proposal did not test this exact clean environment; production integration must still exercise the combined route. Authentication categories are not a billing attestation or a managed-policy audit.


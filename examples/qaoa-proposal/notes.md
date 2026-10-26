# Model notes (model-stated, not verified)

Replaced the removed `qiskit.Aer` import and the 'qasm_simulator' lookup with `qiskit_aer.AerSimulator()`. Dropped the unrecognised `nshots=512` run kwarg. Circuit construction, MaxCut sign, bitstring reversal, and expectation computation are unchanged. Nothing was executed.

## Intentional changes

- Import changed: `from qiskit import QuantumCircuit, Aer` became `from qiskit import QuantumCircuit` plus `from qiskit_aer import AerSimulator`, because `qiskit.Aer` no longer exists in Qiskit 2.x.
- Backend is now `AerSimulator()` (default method) instead of `Aer.get_backend('qasm_simulator')`. The legacy QasmSimulator is a different class. Sampling semantics should be the same, but this is a different backend object.
- Removed the `nshots=512` argument from `backend.run(...)`. It is not an Aer option (the option is `shots`), so it was most likely ignored before. Removing it should not change behaviour, but it is a code change.
- Deliberately did NOT 'fix' the shots handling. `backend.shots = shots` is kept as a plain attribute with no effect on execution, and the `shots` argument still does not control the sample count. Runs use the Aer default of 1024 shots, as in the source (assuming the old `nshots` kwarg was ignored).

## Uncertainties

- I assumed the old `nshots=512` kwarg was silently ignored in aer 0.14.2, so the effective shot count was the default 1024, not 512. If it was honoured in some way, the old counts differ from the new ones. Please confirm which is intended. If you want `shots` honoured, use `backend.run(qc, shots=shots, seed_simulator=10)`. That would be a behaviour change.
- With `seed_simulator=10`, exact counts and expectation values may differ from 0.14.2 because the RNG, backend internals, or default simulation method can change between aer versions. Statistical behaviour should match, but bit-for-bit reproduction is not guaranteed.
- Nodes are assumed to be labelled 0..n-1, as in the source. Other labels would fail in `rzz` and in bitstring indexing, exactly as before.
- I did not add an explicit `transpile` step. I believe Aer 0.18 accepts h, rx, rzz and measure directly, but I could not run it to verify.

# Port notes: legacy_functions.py -> port_functions.py

Target: Qiskit 2.6.1, qiskit-aer 0.18.0. Nothing was executed; port written offline and untested.

## Preserved unchanged
- `maxcut_obj`, `compute_expectation`, `create_qaoa_circ` bodies are byte-for-byte the legacy code.
- Signatures: `maxcut_obj(x, G)`, `compute_expectation(counts, G)`, `create_qaoa_circ(G, theta)`, `get_expectation(G, shots=512)`.
- Angle ordering: `beta = theta[:p]`, `gamma = theta[p:]`, `p = len(theta)//2`. Odd-length `theta` still puts the extra element at the end of `gamma` (unused, as before).
- Circuit: H on all qubits; per layer `rzz(2*gamma)` over `G.edges()` in edge order, then `rx(2*beta)` on every qubit; `measure_all()`.
- Objective: negative cut size (minimized). Bitstring reversal (`bitstring[::-1]`) kept, mapping Qiskit little-endian keys to node index.
- Graph support: nodes must be integers 0..n-1 (qubit count = `len(G.nodes())`, `x[i]` indexing). Edge weights ignored. Self-loops fail as before. Not widened.
- `seed_simulator=10` kept.

## Deliberate behavior changes
1. **Import**: `from qiskit import Aer` removed in Qiskit 1.0+. Now `from qiskit_aer import AerSimulator`.
2. **Backend**: `Aer.get_backend('qasm_simulator')` replaced by `AerSimulator()`. Same method (statevector/automatic) for these circuits; not verified offline.
3. **Explicit transpile**: `transpile(qc, backend, optimization_level=0)` added before `run`. Qiskit 2.x no longer does implicit conversion. Level 0 only decomposes to the backend basis; no circuit-level optimization intended. Aer likely supports `rzz` natively, so this may be a no-op; kept for safety.
4. **Shots (most important)**: legacy set `backend.shots = shots` (arbitrary attribute, no effect on Aer) and passed `nshots=512` to `run` (not a valid Aer option, apparently ignored). Legacy therefore most likely ran Aer's default **1024 shots**, ignoring the `shots` argument. Port passes `shots=shots` to `run`, so default is now **512** and the argument is honored. This follows the documented/intended API but changes sampling noise vs. legacy outputs. To reproduce legacy numerics exactly, call `get_expectation(G, shots=1024)`.
5. **Docstring**: `get_expectation` docstring listed a nonexistent `p` arg; corrected to `G`, `shots`. No code effect.

## Uncertainties
- Legacy effective shots (1024 vs 512) is inferred from knowledge of Aer option handling, not from running it.
- `seed_simulator=10` gives reproducible counts within the new stack, but exact counts need not match legacy runs (different Aer version, simulator class, possible different RNG consumption). Do not expect bit-identical expectation values.
- Not confirmed that `AerSimulator()` default method selection matches `QasmSimulator`'s for all graph sizes.
- `get_counts()` key format assumed to be a single space-free bitstring (true with `measure_all()`, one classical register `meas`).
- Transpile is rebuilt each call to `execute_circ` (as the circuit changes each theta); a performance cost only.

## Could not preserve
- Bit-identical sampled counts with legacy runs (see above).
- Legacy's effective 1024 shots by default (intentionally replaced with the argument value).

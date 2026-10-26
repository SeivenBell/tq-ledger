# Legacy tutorial style (Qiskit 0.4x): GHZ + biased Bell, qiskit.execute, Aer.get_backend, cnot
from math import pi
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute

q = QuantumRegister(3, "q")
c = ClassicalRegister(3, "c")
ghz = QuantumCircuit(q, c, name="ghz")
ghz.h(q[0])
ghz.cnot(q[0], q[1])
ghz.cnot(q[1], q[2])
ghz.barrier()
ghz.measure(q, c)

biased = QuantumCircuit(3, 3, name="biased")
biased.u(pi / 3, 0, 0, 0)         # P(q0=1) = 0.25  (u3 already removed in 0.46)
biased.cnot(0, 1)
biased.x(2)
biased.measure([0, 1, 2], [0, 1, 2])

backend = Aer.get_backend("qasm_simulator")  # NB: aer 0.13.3 + terra 0.46.3 mis-transpiles this batch; needs aer 0.14.2
SHOTS = 4096
result = execute([ghz, biased], backend, shots=SHOTS, seed_simulator=42).result()
for circ in (ghz, biased):
    counts = result.get_counts(circ)
    print(circ.name, "counts", dict(sorted(counts.items())))
    # parity <Z0 Z1 Z2>
    zzz = sum(((-1) ** bits.count("1")) * n for bits, n in counts.items()) / SHOTS
    p_q0 = sum(n for bits, n in counts.items() if bits[-1] == "1") / SHOTS
    print(circ.name, "ZZZ", round(zzz, 4), "P(q0=1)", round(p_q0, 4))

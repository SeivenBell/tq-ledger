# Qiskit 2.x port: if_test replaces c_if; AerSimulator replaces QuantumInstance
from math import pi, sin
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator

THETA = 2 * pi / 5
q = QuantumRegister(3, "q")
c0, c1, out = ClassicalRegister(1, "c0"), ClassicalRegister(1, "c1"), ClassicalRegister(1, "out")
qc = QuantumCircuit(q, c0, c1, out, name="teleport")
qc.ry(THETA, q[0])
qc.h(q[1]); qc.cx(q[1], q[2])
qc.cx(q[0], q[1]); qc.h(q[0])
qc.cx(q[1], q[2]); qc.cz(q[0], q[2])   # deferred-measurement rewrite (equivalent)
qc.measure(q[0], c0[0]); qc.measure(q[1], c1[0])
qc.measure(q[2], out[0])

backend = AerSimulator()
counts = backend.run(transpile(qc, backend, seed_transpiler=7), shots=8192, seed_simulator=7).result().get_counts()
p1 = sum(n for k, n in counts.items() if k.split()[0] == "1") / 8192
print("P(out=1)", round(p1, 3), "expected", round(sin(THETA / 2) ** 2, 3))

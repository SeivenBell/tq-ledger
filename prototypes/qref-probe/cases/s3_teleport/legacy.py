# Legacy teleportation: c_if corrections, QuantumInstance
from math import pi, sin
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer
from qiskit.utils import QuantumInstance

THETA = 2 * pi / 5
q = QuantumRegister(3, "q")
c0, c1, out = ClassicalRegister(1, "c0"), ClassicalRegister(1, "c1"), ClassicalRegister(1, "out")
qc = QuantumCircuit(q, c0, c1, out, name="teleport")
qc.ry(THETA, q[0])            # state to teleport
qc.h(q[1]); qc.cx(q[1], q[2])  # Bell pair
qc.cx(q[0], q[1]); qc.h(q[0])
qc.measure(q[0], c0[0]); qc.measure(q[1], c1[0])
qc.x(q[2]).c_if(c1, 1)
qc.z(q[2]).c_if(c0, 1)
qc.measure(q[2], out[0])

qi = QuantumInstance(Aer.get_backend("aer_simulator"), shots=8192, seed_simulator=7, seed_transpiler=7)
counts = qi.execute(qc).get_counts()
p1 = sum(n for k, n in counts.items() if k.split()[0] == "1") / 8192
print("P(out=1)", round(p1, 3), "expected", round(sin(THETA / 2) ** 2, 3))

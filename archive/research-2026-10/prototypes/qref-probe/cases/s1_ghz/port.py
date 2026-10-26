# Qiskit 2.x port: AerSimulator + transpile + run, u3->u, cnot->cx
from math import pi
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator

q = QuantumRegister(3, "q")
c = ClassicalRegister(3, "c")
ghz = QuantumCircuit(q, c, name="ghz")
ghz.h(q[0])
ghz.cx(q[0], q[1])
ghz.cx(q[1], q[2])
ghz.barrier()
ghz.measure(q, c)

biased = QuantumCircuit(3, 3, name="biased")
biased.u(pi / 3, 0, 0, 0)         # P(q0=1) = 0.25
biased.cx(0, 1)
biased.x(2)
biased.measure([0, 1, 2], [0, 1, 2])

backend = AerSimulator()
SHOTS = 4096
tqcs = transpile([ghz, biased], backend)
result = backend.run(tqcs, shots=SHOTS, seed_simulator=42).result()
for circ in tqcs:
    counts = result.get_counts(circ)
    print(circ.name, "counts", dict(sorted(counts.items())))
    zzz = sum(((-1) ** bits.count("1")) * n for bits, n in counts.items()) / SHOTS
    p_q0 = sum(n for bits, n in counts.items() if bits[-1] == "1") / SHOTS
    print(circ.name, "ZZZ", round(zzz, 4), "P(q0=1)", round(p_q0, 4))

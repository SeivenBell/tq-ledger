# Legacy QAOA p=1 MaxCut grid search: Parameter + bind_parameters + execute
import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit import Parameter

EDGES = [(0, 1), (1, 2), (2, 3), (0, 2)]
N = 4
gamma, beta = Parameter("gamma"), Parameter("beta")
qc = QuantumCircuit(N)
qc.h(range(N))
for i, j in EDGES:
    qc.rzz(2 * gamma, i, j)
for i in range(N):
    qc.rx(2 * beta, i)
qc.measure_all()

def cut_value(bits):
    x = [int(bits[N - 1 - k]) for k in range(N)]   # little-endian: node k <- bits[-1-k]
    return sum(x[i] != x[j] for i, j in EDGES)

gammas = np.linspace(0.1, np.pi - 0.1, 6)
betas = np.linspace(0.1, np.pi / 2 - 0.1, 5)
grid = [(g, b) for g in gammas for b in betas]
bound = [qc.bind_parameters({gamma: g, beta: b}) for g, b in grid]
backend = Aer.get_backend("qasm_simulator")
SHOTS = 2048
res = execute(bound, backend, shots=SHOTS, seed_simulator=11).result()
vals = []
for k in range(len(grid)):
    counts = res.get_counts(k)
    vals.append(sum(cut_value(b) * n for b, n in counts.items()) / SHOTS)
best = int(np.argmax(vals))
print("best gamma", round(grid[best][0], 4), "beta", round(grid[best][1], 4))
print("best expected cut", round(vals[best], 4))
top = max(res.get_counts(best).items(), key=lambda kv: kv[1])[0]
print("most likely bitstring", top, "cut", cut_value(top))

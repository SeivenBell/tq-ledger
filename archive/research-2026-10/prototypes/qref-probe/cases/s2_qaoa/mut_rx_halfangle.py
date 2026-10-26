# Qiskit 2.x port: StatevectorSampler (SamplerV2) with parameter sweep
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorSampler

EDGES = [(0, 1), (1, 2), (2, 3), (0, 2)]
N = 4
gamma, beta = Parameter("gamma"), Parameter("beta")
qc = QuantumCircuit(N)
qc.h(range(N))
for i, j in EDGES:
    qc.rzz(2 * gamma, i, j)
for i in range(N):
    qc.rx(beta, i)
qc.measure_all()

def cut_value(bits):
    x = [int(bits[N - 1 - k]) for k in range(N)]
    return sum(x[i] != x[j] for i, j in EDGES)

gammas = np.linspace(0.1, np.pi - 0.1, 6)
betas = np.linspace(0.1, np.pi / 2 - 0.1, 5)
grid = [(g, b) for g in gammas for b in betas]
SHOTS = 2048
sampler = StatevectorSampler(seed=11)
# SamplerV2 binds positionally in qc.parameters order (sorted by name)
col = {gamma: 0, beta: 1}
param_values = np.array([[gb[col[p]] for p in qc.parameters] for gb in grid])
job = sampler.run([(qc, param_values)], shots=SHOTS)
data = job.result()[0].data.meas
vals = []
for k in range(len(grid)):
    counts = data[k].get_counts()
    vals.append(sum(cut_value(b) * n for b, n in counts.items()) / SHOTS)
best = int(np.argmax(vals))
print("best gamma", round(grid[best][0], 4), "beta", round(grid[best][1], 4))
print("best expected cut", round(vals[best], 4))
top = max(data[best].get_counts().items(), key=lambda kv: kv[1])[0]
print("most likely bitstring", top, "cut", cut_value(top))

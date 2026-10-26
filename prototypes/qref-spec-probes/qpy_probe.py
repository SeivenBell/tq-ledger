import io
import json
import math
from importlib.metadata import version
from qiskit import QuantumCircuit, qpy

circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.cx(0, 1)
circuit.global_phase = math.pi / 3
circuit.measure([0, 1], [0, 1])
stream = io.BytesIO()
qpy.dump(circuit, stream)
payload = stream.getvalue()
restored = qpy.load(io.BytesIO(payload))[0]
assert restored == circuit
assert float(restored.global_phase) == float(circuit.global_phase)
print(json.dumps({"qiskit_version": version("qiskit"), "snapshot_bytes": len(payload), "same_runtime_roundtrip_equal": restored == circuit, "global_phase_retained": float(restored.global_phase) == float(circuit.global_phase)}, sort_keys=True))

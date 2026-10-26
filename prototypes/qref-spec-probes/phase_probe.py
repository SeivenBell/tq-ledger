import json,math
from qiskit import QuantumCircuit
from mqt import qcec
base=QuantumCircuit(1); base.h(0)
global_phase=base.copy(); global_phase.global_phase=math.pi/2
relative_phase=base.copy(); relative_phase.z(0)
gate_global_phase=QuantumCircuit(1); gate_global_phase.x(0); gate_global_phase.z(0); gate_global_phase.x(0); gate_global_phase.z(0); gate_global_phase.h(0)
print(json.dumps({name:str(qcec.verify(base,circuit).equivalence) for name,circuit in [('identity',base),('global_phase_metadata',global_phase),('relative_phase_z',relative_phase),('gate_global_minus_one',gate_global_phase)]},indent=2))

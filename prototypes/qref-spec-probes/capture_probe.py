"""THROWAWAY planning probe: actual Aer submission capture, not production QRef."""
import importlib.util
import json
from pathlib import Path
import sys

import networkx as nx
from qiskit import QuantumCircuit, qasm2
from qiskit.quantum_info import Statevector
from qiskit_aer.backends.aerbackend import AerBackend

module_path, destination = map(Path, sys.argv[1:3])
spec = importlib.util.spec_from_file_location("inspected_helpers", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
graphs = {
    "textbook_cycle4": [(0, 1), (1, 2), (2, 3), (3, 0)],
    "asymmetric4": [(0, 1), (1, 2), (2, 3), (0, 2)],
    "cycle5": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)],
}
angles = [[0.17, 0.63], [0.81, 0.29], [0.17, 0.63, 0.41, 0.92]]
original_run = AerBackend.run
captures = []


def capture_run(backend, circuits, *args, **kwargs):
    submitted = [circuits] if isinstance(circuits, QuantumCircuit) else list(circuits)
    assert len(submitted) == 1
    capture = {"circuit": submitted[0].copy(), "options": dict(kwargs)}
    captures.append(capture)
    capture["job"] = original_run(backend, circuits, *args, **kwargs)
    return capture["job"]


def negative_cut(integer, edges):
    return -sum(((integer >> u) & 1) != ((integer >> v) & 1) for u, v in edges)


records = []
truth_tables = []
AerBackend.run = capture_run
try:
    for graph_id, edges in graphs.items():
        graph = nx.Graph(edges)
        n = len(graph)
        for integer in range(2**n):
            node_order = "".join(str((integer >> i) & 1) for i in range(n))
            qiskit_order = format(integer, f"0{n}b")
            expected = negative_cut(integer, edges)
            assert module.maxcut_obj(node_order, graph) == expected
            assert module.compute_expectation({qiskit_order: 1}, graph) == expected
        truth_tables.append({"graph": graph_id, "assignments": 2**n})
        for theta in angles:
            for requested in [512, 17]:
                captures.clear()
                returned = module.get_expectation(graph, shots=requested)(theta)
                assert len(captures) == 1
                capture = captures[0]
                circuit = capture["circuit"]
                measurement_map = [
                    [circuit.find_bit(instruction.qubits[0]).index,
                     circuit.find_bit(instruction.clbits[0]).index]
                    for instruction in circuit.data
                    if instruction.operation.name == "measure"
                ]
                assert sorted(measurement_map) == [[i, i] for i in range(n)]
                result = capture["job"].result()
                counts = result.get_counts()
                decoded = sum(negative_cut(int(bits, 2), edges) * count
                              for bits, count in counts.items()) / sum(counts.values())
                assert abs(returned - decoded) <= 1e-10
                pure = circuit.remove_final_measurements(inplace=False)
                probabilities = Statevector.from_instruction(pure).probabilities_dict()
                records.append({
                    "key": [graph_id, theta, requested],
                    "executed_shots": result.results[0].shots,
                    "count_sum": sum(counts.values()),
                    "counts": counts,
                    "measurement_map": measurement_map,
                    "returned_objective": returned,
                    "independent_objective": decoded,
                    "actual_submitted_qasm": qasm2.dumps(pure),
                    "probabilities": probabilities,
                    "run_options": capture["options"],
                })
finally:
    AerBackend.run = original_run

destination.write_text(json.dumps({"executions": records, "truth_tables": truth_tables}, indent=2))
print(json.dumps({"executions": len(records), "truth_table_assignments": sum(t["assignments"] for t in truth_tables),
                  "executed_shots": sorted({r["executed_shots"] for r in records})}))

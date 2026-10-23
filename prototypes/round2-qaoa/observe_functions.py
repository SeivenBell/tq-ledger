"""Throwaway experiment: inspect textbook QAOA functions, not a general verifier."""
import importlib.util
import json
import pathlib
import sys

import networkx as nx
from qiskit import qasm2
from qiskit.quantum_info import Statevector

module_path, output_path = map(pathlib.Path, sys.argv[1:3])
spec = importlib.util.spec_from_file_location("observed_functions", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

graphs = {
    "textbook_cycle4": [(0, 1), (1, 2), (2, 3), (3, 0)],
    "asymmetric4": [(0, 1), (1, 2), (2, 3), (0, 2)],
    "cycle5": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)],
}
angles = [[0.17, 0.63], [0.81, 0.29], [0.17, 0.63, 0.41, 0.92]]
records = []
for name, edges in graphs.items():
    graph = nx.Graph(edges)
    for theta in angles:
        circuit = module.create_qaoa_circ(graph, theta)
        pure = circuit.remove_final_measurements(inplace=False)
        probabilities = Statevector.from_instruction(pure).probabilities_dict()
        for requested_shots in [512, 17]:
            objective = module.get_expectation(graph, shots=requested_shots)
            captures = {}
            closure = dict(zip(objective.__code__.co_freevars,
                               (cell.cell_contents for cell in objective.__closure__)))
            backend = closure["backend"]
            original_run = backend.run

            def observe_run(*args, **kwargs):
                captures["options"] = kwargs
                captures["job"] = original_run(*args, **kwargs)
                return captures["job"]

            backend.run = observe_run
            sampled_objective = objective(theta)
            result = captures["job"].result()
            counts = result.get_counts()
            records.append({
                "key": [name, theta, requested_shots],
                "qubits": circuit.num_qubits,
                "requested_shots": requested_shots,
                "executed_shots": result.results[0].shots,
                "count_sum": sum(counts.values()),
                "run_options": captures["options"],
                "sampled_objective": sampled_objective,
                "exact_objective": module.compute_expectation(probabilities, graph),
                "probabilities": probabilities,
                "unitary_qasm": qasm2.dumps(pure),
            })
output_path.write_text(json.dumps(records, indent=2))
print(json.dumps({"module": str(module_path), "observations": len(records),
                  "shot_pairs": sorted({(x["requested_shots"], x["executed_shots"])
                                        for x in records}),
                  "first_exact_objective": records[0]["exact_objective"],
                  "output": str(output_path)}, indent=2))

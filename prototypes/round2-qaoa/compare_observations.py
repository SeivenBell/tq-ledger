"""Throwaway comparison of a real notebook port; not whole-program certification."""
import json
from pathlib import Path

from mqt import qcec
from qiskit import qasm2

root = Path(__file__).parent
left = json.loads((root / "legacy-observations.json").read_text())
right = json.loads((root / "modern-observations.json").read_text())
assert [r["key"] for r in left] == [r["key"] for r in right]
results = []
for original, port in zip(left, right):
    if original["requested_shots"] != 512:
        continue
    circuit_result = qcec.verify(
        qasm2.loads(original["unitary_qasm"], custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS),
        qasm2.loads(port["unitary_qasm"], custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS))
    keys = set(original["probabilities"]) | set(port["probabilities"])
    max_probability_difference = max(abs(original["probabilities"].get(k, 0.0)
                                         - port["probabilities"].get(k, 0.0)) for k in keys)
    results.append({
        "key": original["key"][:2],
        "qcec_result": str(circuit_result.equivalence),
        "max_probability_difference": max_probability_difference,
        "exact_objective_difference": abs(original["exact_objective"] - port["exact_objective"]),
    })
report = {
    "circuit_checks": results,
    "observed_shot_changes": [{"requested": a["requested_shots"],
                               "original_executed": a["executed_shots"],
                               "port_executed": b["executed_shots"]}
                              for a, b in zip(left, right)
                              if a["executed_shots"] != b["executed_shots"]],
    "scope": "Nine fixed circuit/parameter cases; 18 sampled executions per runtime; no optimizer, hardware or whole-program proof",
}
(root / "comparison.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))

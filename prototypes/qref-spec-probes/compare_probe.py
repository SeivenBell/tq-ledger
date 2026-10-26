"""THROWAWAY planning probe: compare actual submitted circuits, not production QRef."""
import json
from pathlib import Path
import sys

from mqt import qcec
from qiskit import qasm2

reference_path, target_path, destination = map(Path, sys.argv[1:4])
reference = json.loads(reference_path.read_text())["executions"]
target = json.loads(target_path.read_text())["executions"]
assert len(reference) == len(target) == 18
assert [r["key"] for r in reference] == [r["key"] for r in target]
checks = {}
for left, right in zip(reference, target):
    key = (left["actual_submitted_qasm"], right["actual_submitted_qasm"])
    if key not in checks:
        result = qcec.verify(
            qasm2.loads(key[0], custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS),
            qasm2.loads(key[1], custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS))
        checks[key] = {"criterion": str(result.equivalence), "execution_keys": []}
    checks[key]["execution_keys"].append(left["key"])
    assert left["measurement_map"] == right["measurement_map"]
    assert max(abs(left["probabilities"].get(bits, 0) - right["probabilities"].get(bits, 0))
               for bits in set(left["probabilities"]) | set(right["probabilities"])) <= 1e-10
assert all(row["criterion"] == "EquivalenceCriterion.equivalent" for row in checks.values())
record = {"actual_submitted_circuit_checks": list(checks.values()),
          "observations_per_runtime": len(reference),
          "reference_shots": sorted({r["executed_shots"] for r in reference}),
          "target_shots": sorted({r["executed_shots"] for r in target}),
          "limit": "Positive feasibility only; no failure states, full metadata, product protocol or sandbox tested"}
destination.write_text(json.dumps(record, indent=2))
print(json.dumps({"distinct_submitted_pairs": len(checks), "covered_executions": len(reference),
                  "all_circuit_results_equivalent": True}))

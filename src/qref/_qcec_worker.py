"""Standalone QCEC worker: compares two measurement-free QASM2 files.

Runs in the checker interpreter with ``python -I``; never imports qref or candidate code.
Usage: python -I _qcec_worker.py REFERENCE.qasm TARGET.qasm
Prints one JSON object.
"""
import json
import sys
from importlib import metadata
from pathlib import Path

from mqt import qcec
from qiskit import qasm2

reference = qasm2.loads(Path(sys.argv[1]).read_text(encoding="utf-8"),
                        custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS)
target = qasm2.loads(Path(sys.argv[2]).read_text(encoding="utf-8"),
                     custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS)
result = qcec.verify(reference, target)
print(json.dumps({
    "criterion": str(result.equivalence).rsplit(".", 1)[-1],
    "checker_version": metadata.version("mqt-qcec"),
    "qiskit_version": metadata.version("qiskit"),
}))

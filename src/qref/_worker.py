"""Standalone QRef observation worker.

Runs inside a pinned candidate interpreter with ``python -I``. It must import only
stdlib and the candidate's quantum dependencies, never the qref package.

Usage: python -I _worker.py RUNTIME_JSON OUT_DIR
"""
import importlib.util
import io
import json
import os
import platform
import sys
import traceback
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_json_atomic(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def environment():
    dists = sorted(
        {(d.metadata["Name"] or "").lower().replace("_", "-"): d.version for d in metadata.distributions()}.items()
    )
    return {
        "python_version": platform.python_version(),
        "os": platform.system(),
        "architecture": platform.machine(),
        "distributions": [{"name": n, "version": v} for n, v in dists if n],
    }


def json_safe(value):
    try:
        json.dumps(value, allow_nan=False)
        return value
    except (TypeError, ValueError):
        return {"unsupported_type": type(value).__module__ + "." + type(value).__qualname__}


class UnsupportedExecution(Exception):
    def __init__(self, code, detail):
        super().__init__(detail)
        self.code = code


def main():
    runtime = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    side = runtime["side"]
    doc = {
        "schema": "qref.qaoa-observations/v1",
        "side": side,
        "module_sha256": runtime["module_sha256"],
        "environment": environment(),
        "started_at": now(),
        "finished_at": None,
        "import": {"state": "not_run", "reason_code": None, "error_ref": None},
        "executions": [
            {"id": e["id"], "input_sha256": e["input_sha256"], "state": "not_run", "reason_code": None,
             "started_at": None, "finished_at": None, "circuit": None, "sampling": None, "numeric": None,
             "error_ref": None}
            for e in runtime["executions"]
        ],
        "classical_tables": [],
    }
    doc_path = out / "observations.json"
    write_json_atomic(doc_path, doc)

    import networkx as nx
    from qiskit import QuantumCircuit, qasm2, qpy
    from qiskit.quantum_info import Statevector
    from qiskit_aer.backends.aerbackend import AerBackend

    original_run = AerBackend.run
    state = {"active": False, "captures": []}

    def capture_run(backend, circuits, *args, **kwargs):
        if not state["active"]:
            raise UnsupportedExecution("import_time_execution", "AerBackend.run called outside a declared execution")
        submitted = [circuits] if isinstance(circuits, QuantumCircuit) else list(circuits)
        record = {
            "circuits": [c.copy() for c in submitted],
            "backend_class": type(backend).__module__ + "." + type(backend).__qualname__,
            "run_kwargs": {k: json_safe(v) for k, v in sorted(kwargs.items())},
            "positional_count": len(args),
        }
        state["captures"].append(record)
        record["job"] = original_run(backend, circuits, *args, **kwargs)
        return record["job"]

    AerBackend.run = capture_run
    try:
        doc["import"]["state"] = "incomplete"
        write_json_atomic(doc_path, doc)
        try:
            spec = importlib.util.spec_from_file_location("qref_candidate", runtime["module_path"])
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except UnsupportedExecution as exc:
            doc["import"].update(state="unsupported", reason_code=exc.code)
            raise SystemExit(finish(doc, doc_path, out, "import", exc))
        except BaseException as exc:  # candidate code: record any import failure
            doc["import"].update(state="failed", reason_code="import_failed")
            raise SystemExit(finish(doc, doc_path, out, "import", exc))
        doc["import"]["state"] = "completed"

        graphs = {}
        for g in runtime["graphs"]:
            graph = nx.Graph()
            graph.add_nodes_from(g["nodes"])
            graph.add_edges_from(g["edges"])
            graphs[g["id"]] = graph
            n = len(g["nodes"])
            rows = []
            for k in range(2 ** n):
                node_order = "".join(str((k >> i) & 1) for i in range(n))
                qiskit_order = format(k, f"0{n}b")
                rows.append({
                    "k": k,
                    "maxcut_obj": float(module.maxcut_obj(node_order, graph)),
                    "compute_expectation": float(module.compute_expectation({qiskit_order: 1}, graph)),
                })
            doc["classical_tables"].append({"graph_id": g["id"], "n": n, "rows": rows})
        write_json_atomic(doc_path, doc)

        for spec_e, rec in zip(runtime["executions"], doc["executions"]):
            rec["state"] = "incomplete"
            rec["started_at"] = now()
            write_json_atomic(doc_path, doc)
            try:
                observe(spec_e, rec, module, graphs[spec_e["graph_id"]], state, out, qasm2, qpy, Statevector)
                rec["state"] = "completed"
                rec["reason_code"] = None
            except UnsupportedExecution as exc:
                rec["state"] = "unsupported"
                rec["reason_code"] = exc.code
                rec["error_ref"] = write_error(out, spec_e["id"], exc)
            except BaseException as exc:
                rec["state"] = "failed"
                rec["reason_code"] = "worker_failed"
                rec["error_ref"] = write_error(out, spec_e["id"], exc)
            finally:
                state["active"] = False
                state["captures"].clear()
                rec["finished_at"] = now()
                write_json_atomic(doc_path, doc)
    finally:
        AerBackend.run = original_run
    doc["finished_at"] = now()
    write_json_atomic(doc_path, doc)


def finish(doc, doc_path, out, scope, exc):
    doc["import"]["error_ref"] = write_error(out, scope, exc)
    for rec in doc["executions"]:
        rec["reason_code"] = "import_failed"
    doc["finished_at"] = now()
    write_json_atomic(doc_path, doc)
    return 0


def write_error(out, scope, exc):
    name = "error-" + scope.replace("/", "_") + ".txt"
    text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    (out / name).write_text(text[-20000:], encoding="utf-8")
    return name


def observe(spec_e, rec, module, graph, state, out, qasm2, qpy, Statevector):
    n = graph.number_of_nodes()
    state["captures"].clear()
    state["active"] = True
    returned = module.get_expectation(graph, shots=spec_e["requested_shots"])(spec_e["theta"])
    state["active"] = False
    caps = state["captures"]
    if len(caps) != 1 or len(caps[0]["circuits"]) != 1:
        raise UnsupportedExecution(
            "unsupported_backend_execution",
            f"expected exactly one backend run with one circuit, got {len(caps)} runs",
        )
    cap = caps[0]
    circuit = cap["circuits"][0]
    stem = spec_e["id"].replace("/", "__")
    qpy_buf = io.BytesIO()
    qpy.dump(circuit, qpy_buf)
    (out / f"{stem}.qpy").write_bytes(qpy_buf.getvalue())

    measurement_map = []
    tail_started = False
    shape_problem = None
    for inst in circuit.data:
        name = inst.operation.name
        if name == "measure":
            tail_started = True
            measurement_map.append([circuit.find_bit(inst.qubits[0]).index, circuit.find_bit(inst.clbits[0]).index])
        elif name == "barrier":
            continue
        elif tail_started:
            shape_problem = ("unsupported_measurement", f"operation {name} after measurement")
        elif name in ("reset", "if_else", "while_loop", "for_loop", "switch_case", "initialize"):
            shape_problem = ("unsupported_circuit", f"unsupported operation {name}")
    metadata_doc = {
        "num_qubits": circuit.num_qubits,
        "num_clbits": circuit.num_clbits,
        "classical_registers": [[r.name, r.size] for r in circuit.cregs],
        "measurement_map": measurement_map,
        "layout": None if circuit.layout is None else str(circuit.layout),
        "global_phase": float(circuit.global_phase),
        "num_parameters": circuit.num_parameters,
    }
    (out / f"{stem}.circuit.json").write_text(json.dumps(metadata_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if shape_problem is None:
        if circuit.num_qubits != n or circuit.num_clbits != n or len(circuit.cregs) != 1:
            shape_problem = ("unsupported_measurement", "dimensions or classical registers differ from the declared graph")
        elif sorted(measurement_map) != [[i, i] for i in range(n)]:
            shape_problem = ("unsupported_measurement", "terminal measurement map is not identity")
        elif circuit.layout is not None:
            shape_problem = ("unsupported_layout", "circuit carries a layout")
        elif circuit.num_parameters:
            shape_problem = ("unsupported_circuit", "unbound parameters")
    result = cap["job"].result()
    counts = {str(k): int(v) for k, v in result.get_counts().items()}
    completed = int(result.results[0].shots)
    rec["sampling"] = {
        "requested_shots": spec_e["requested_shots"],
        "completed_shots": completed,
        "count_sum": sum(counts.values()),
        "counts": dict(sorted(counts.items())),
        "backend_class": cap["backend_class"],
        "run_kwargs": cap["run_kwargs"],
    }
    rec["circuit"] = {"qpy": f"{stem}.qpy", "metadata": f"{stem}.circuit.json", "qasm": None, **metadata_doc}
    if shape_problem:
        raise UnsupportedExecution(*shape_problem)
    pure = circuit.remove_final_measurements(inplace=False)
    (out / f"{stem}.qasm").write_text(qasm2.dumps(pure), encoding="utf-8")
    rec["circuit"]["qasm"] = f"{stem}.qasm"
    probs_dict = Statevector.from_instruction(pure).probabilities_dict()
    probabilities = [float(probs_dict.get(format(k, f"0{n}b"), 0.0)) for k in range(2 ** n)]
    exact_for_module = {format(k, f"0{n}b"): p for k, p in enumerate(probabilities) if p > 0}
    rec["numeric"] = {
        "returned": float(returned),
        "module_on_counts": float(module.compute_expectation(counts, graph)),
        "probabilities": probabilities,
        "module_on_probabilities": float(module.compute_expectation(exact_for_module, graph)),
    }


if __name__ == "__main__":
    main()

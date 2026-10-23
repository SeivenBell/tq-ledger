"""QRef tracer: run a Qiskit script (legacy 0.4x or 2.x) under instrumentation.

usage: python qref/trace.py OUT.json SCRIPT.py [--replay]

Captures every circuit that reaches an execution boundary
  * qiskit_aer AerBackend.run          (execute(), QuantumInstance, backend.run)
  * qiskit.primitives.StatevectorSampler.run   (SamplerV2 pubs, positional binding)
and for each bound circuit records
  * exact clbit distribution (static circuits: all measurements terminal, no feed-forward)
  * referee counts: REF_SHOTS on a fresh AerSimulator with a fixed seed (any circuit)
--replay replaces sampled results with deterministic "ideal counts"
(largest-remainder rounding of the exact distribution) so classical post-processing
in legacy and port sees identical data and printed outputs become comparable.
"""
import contextlib
import io
import json
import runpy
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")

REF_SHOTS = 20000
REF_SEED = 1234

from qiskit import QuantumCircuit, transpile  # noqa: E402
from qiskit.quantum_info import Statevector  # noqa: E402
from qiskit_aer import AerSimulator  # noqa: E402
from qiskit_aer.backends.aerbackend import AerBackend  # noqa: E402

RECORDS = []
REPLAY = "--replay" in sys.argv
_inside = [False]


def _bitidx(circ, bit):
    return circ.find_bit(bit).index


def _is_dynamic(op):
    if getattr(op, "condition", None) is not None:  # legacy c_if
        return True
    return op.name in ("if_else", "while_loop", "for_loop", "switch_case", "reset")


def exact_distribution(circ):
    """Return {clbit-string: prob} or None if circuit is not static."""
    measured = {}  # qubit -> clbit
    body = QuantumCircuit(circ.num_qubits)
    for inst in circ.data:
        op = inst.operation
        qs = [_bitidx(circ, q) for q in inst.qubits]
        if _is_dynamic(op):
            return None
        if op.name == "barrier":
            continue
        if op.name == "measure":
            measured[qs[0]] = _bitidx(circ, inst.clbits[0])
            continue
        if any(q in measured for q in qs):  # gate after measurement -> mid-circuit
            return None
        body.append(op, qs)
    probs = Statevector(body).probabilities()
    out = {}
    ncl = circ.num_clbits
    for idx, p in enumerate(probs):
        if p < 1e-15:
            continue
        cl = [0] * ncl
        for q, c in measured.items():
            cl[c] = (idx >> q) & 1
        key = "".join(str(b) for b in reversed(cl))
        out[key] = out.get(key, 0.0) + float(p)
    return out


def ideal_counts(dist, shots):
    keys = sorted(dist)
    raw = np.array([dist[k] * shots for k in keys])
    base = np.floor(raw).astype(int)
    rem = shots - base.sum()
    order = np.argsort(-(raw - base), kind="stable")
    base[order[:rem]] += 1
    return {k: int(n) for k, n in zip(keys, base) if n}


_ref_backend = AerSimulator()


def record(circ, source):
    dist = exact_distribution(circ)
    _inside[0] = True
    try:
        tc = transpile(circ, _ref_backend, optimization_level=0)
        res = _ORIG_RUN(_ref_backend, tc, shots=REF_SHOTS, seed_simulator=REF_SEED).result()
        ref = {k.replace(" ", ""): int(v) for k, v in res.get_counts().items()}
    finally:
        _inside[0] = False
    RECORDS.append(
        {
            "index": len(RECORDS),
            "source": source,
            "name": circ.name,
            "num_qubits": circ.num_qubits,
            "num_clbits": circ.num_clbits,
            "ops": dict(circ.count_ops()),
            "static": dist is not None,
            "exact": dist,
            "ref_counts": ref,
        }
    )
    return dist


# ---- hook 1: Aer backends (covers execute(), QuantumInstance, backend.run) ----
_ORIG_RUN = AerBackend.run


def _hex(bits):
    return hex(int(bits, 2))


def traced_run(self, circuits, *args, **kwargs):
    if _inside[0]:
        return _ORIG_RUN(self, circuits, *args, **kwargs)
    circs = circuits if isinstance(circuits, (list, tuple)) else [circuits]
    dists = [record(c, "AerBackend.run") for c in circs]
    job = _ORIG_RUN(self, circuits, *args, **kwargs)
    if REPLAY:
        result = job.result()  # AerJob caches its Result; mutate in place
        for exp, dist in zip(result.results, dists):
            if dist is None:
                continue
            shots = exp.shots if isinstance(exp.shots, int) else exp.shots[1] - exp.shots[0]
            exp.data.counts = {_hex(k): v for k, v in ideal_counts(dist, shots).items()}
    return job


AerBackend.run = traced_run

# ---- hook 2: SamplerV2 reference primitive (Qiskit >= 1.x only) ----
try:
    from qiskit.primitives import StatevectorSampler
    from qiskit.primitives.containers.sampler_pub import SamplerPub

    _ORIG_SV_RUN = StatevectorSampler.run

    def traced_sv_run(self, pubs, *, shots=None):
        for pub in pubs:
            pub = SamplerPub.coerce(pub, shots)
            pv = pub.parameter_values
            if pv.num_parameters == 0:
                record(pub.circuit, "StatevectorSampler.run")
                continue
            arr = pv.as_array(pub.circuit.parameters)  # positional, circuit.parameters order
            for row in arr.reshape(-1, arr.shape[-1]):
                record(pub.circuit.assign_parameters(row), "StatevectorSampler.run")
        return _ORIG_SV_RUN(self, pubs, shots=shots)

    StatevectorSampler.run = traced_sv_run

    if REPLAY:
        _ORIG_SAMPLE = Statevector.sample_memory

        def replay_sample_memory(self, shots, qargs=None):
            probs = self.probabilities_dict(qargs)
            counts = ideal_counts(probs, shots)
            return np.array([k for k, n in counts.items() for _ in range(n)])

        Statevector.sample_memory = replay_sample_memory
except ImportError:
    pass


def main():
    out, script = sys.argv[1], sys.argv[2]
    buf = io.StringIO()
    err = None
    with contextlib.redirect_stdout(buf):
        try:
            runpy.run_path(script, run_name="__main__")
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__}: {e}"
    import qiskit

    json.dump(
        {
            "script": script,
            "qiskit": qiskit.__version__,
            "replay": REPLAY,
            "error": err,
            "stdout": buf.getvalue(),
            "circuits": RECORDS,
        },
        open(out, "w"),
        indent=1,
    )
    print(f"traced {script}: {len(RECORDS)} circuits, qiskit {qiskit.__version__}, error={err}")


if __name__ == "__main__":
    main()

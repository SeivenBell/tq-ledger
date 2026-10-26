"""Shared record rules: parsing, validation, canonical identity and exact-byte hashing."""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from importlib import resources
from pathlib import Path

import jsonschema


class ContractError(ValueError):
    """A record violates the QRef protocol."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def canonical_sha256(value) -> str:
    return sha256_bytes(canonical(value))


def record_bytes(value) -> bytes:
    """Exact on-disk form for evidence/manifests; their identity is the SHA-256 of these bytes."""
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def _reject_duplicates(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ContractError(f"duplicate JSON key: {key}")
        seen[key] = value
    return seen


def _reject_constant(token):
    raise ContractError(f"non-finite number: {token}")


def load_json_bytes(data: bytes):
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=_reject_duplicates, parse_constant=_reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"invalid JSON: {exc}") from exc


def _schema():
    text = resources.files("qref").joinpath("protocol.schema.json").read_text(encoding="utf-8")
    return json.loads(text)


def validate(kind: str, value) -> None:
    schema = _schema()
    sub = {"$ref": f"#/definitions/{kind}", "definitions": schema["definitions"]}
    errors = sorted(jsonschema.Draft7Validator(sub).iter_errors(value), key=lambda e: list(e.absolute_path))
    if errors:
        e = errors[0]
        where = "/".join(str(p) for p in e.absolute_path) or "(root)"
        raise ContractError(f"{kind} invalid at {where}: {e.message}")


def validate_case(case: dict) -> None:
    validate("case", case)
    for side in ("reference", "target"):
        r = case[side]["receipt"]
        if r["kind"] == "upstream_extract" and not all(r[k] for k in ("upstream_url", "upstream_revision", "upstream_path")):
            raise ContractError(f"{side}: upstream_extract requires upstream url, revision and path")
    for field in ("graphs", "angles"):
        ids = [item["id"] for item in case[field]]
        if len(ids) != len(set(ids)):
            raise ContractError(f"duplicate {field} id")
    for shot in case["shots"]:
        if isinstance(shot, bool):
            raise ContractError("shots must be integers, not booleans")
    for g in case["graphs"]:
        n = len(g["nodes"])
        if g["nodes"] != list(range(n)):
            raise ContractError(f"graph {g['id']}: nodes must be exactly 0..n-1")
        seen = set()
        for u, v in g["edges"]:
            if u == v or not (u < n and v < n):
                raise ContractError(f"graph {g['id']}: invalid edge {[u, v]}")
            key = frozenset((u, v))
            if key in seen:
                raise ContractError(f"graph {g['id']}: duplicate edge {[u, v]}")
            seen.add(key)
    for a in case["angles"]:
        if len(a["theta"]) % 2 or any(isinstance(t, bool) or not math.isfinite(t) for t in a["theta"]):
            raise ContractError(f"angles {a['id']}: theta must be finite with even length")
    if len(case["graphs"]) * len(case["angles"]) * len(case["shots"]) > 64:
        raise ContractError("a case is limited to 64 executions per side")


def load_case(path: Path) -> tuple[dict, bytes]:
    data = path.read_bytes()
    case = load_json_bytes(data)
    validate_case(case)
    return case, data


def expected_executions(case: dict) -> list[dict]:
    rows = []
    for g in case["graphs"]:
        for a in case["angles"]:
            for shots in case["shots"]:
                inputs = {
                    "graph": {"nodes": g["nodes"], "edges": g["edges"]},
                    "theta": a["theta"],
                    "requested_shots": shots,
                    "interpretation": case["interpretation"],
                }
                rows.append({
                    "id": f"{g['id']}/{a['id']}/shots-{shots}",
                    "graph_id": g["id"],
                    "angle_id": a["id"],
                    "nodes": g["nodes"],
                    "edges": g["edges"],
                    "theta": a["theta"],
                    "requested_shots": shots,
                    "input_sha256": canonical_sha256(inputs),
                })
    return rows


def read_pins(path: Path) -> dict[str, str]:
    pins = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        name, sep, version = line.partition("==")
        if not sep:
            raise ContractError(f"{path.name}: only exact name==version pins are supported: {line}")
        pins[name.strip().lower().replace("_", "-")] = version.strip()
    return pins

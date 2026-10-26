"""Command-line routes. Policy lives in the modules; this file only parses options."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import contracts


def summary(out: Path) -> str:
    """Short terminal view of a finished run, read back from its evidence record."""
    import json
    e = json.loads((out / "evidence.json").read_text(encoding="utf-8"))
    circuits = [c for c in e["checks"] if c["kind"] == "circuit"]
    equivalent = sum(c["status"] == "pass" for c in circuits)
    pairs = len(e["circuit_results"])
    cov = e["coverage"]
    lines = [
        f"run state: {e['run_state']}   evidence: {e['evidence_summary']}   "
        f"{cov['completed_pairs']}/{len(cov['expected_executions'])} execution pairs completed",
        f"circuits:  {equivalent}/{len(circuits)} executions equivalent ({pairs} distinct submitted-circuit pairs checked)",
        "checks:    " + ", ".join(f"{n} {s}" for s, n in e["status_counts"].items() if n),
    ]
    for f in e["findings"]:
        n = len(f["check_ids"])
        lines.append(f"finding:   {f['title']} ({n} check{'s' if n != 1 else ''})")
    if not e["findings"]:
        lines.append("finding:   none")
    lines.append("human decision: not recorded")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="qref", description="Reviewable evidence for an AI-assisted Qiskit migration.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("propose", help="Ask the local Claude CLI (existing subscription) for a proposed port. Never executes it.")
    p.add_argument("--case", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True, help="new directory")

    r = sub.add_parser("run", help="Execute reference and target in their pinned interpreters and record evidence.")
    r.add_argument("--case", type=Path, required=True)
    r.add_argument("--reference-python", type=Path, required=True)
    r.add_argument("--target-python", type=Path, required=True, help="also runs the QCEC circuit checker")
    r.add_argument("--out", type=Path, required=True, help="new directory")
    r.add_argument("--trust-local-code", action="store_true",
                   help="required: candidate Python can read local files, use the network and access process credentials")

    rep = sub.add_parser("report", help="Verify a bundle, optionally attach a human decision file, and render into a new directory.")
    rep.add_argument("--run", type=Path, required=True)
    rep.add_argument("--decisions", type=Path, help="filled-in copy of review-template.json (qref.decisions/v1)")
    rep.add_argument("--out", type=Path, required=True)

    v = sub.add_parser("verify-bundle", help="Check a bundle directory against its manifest and evidence links.")
    v.add_argument("--run", type=Path, required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "propose":
            from . import proposal
            return proposal.propose(args.case, args.out)
        if args.command == "run":
            from . import execution
            code = execution.run(args.case, args.reference_python, args.target_python, args.out, args.trust_local_code)
            print(summary(args.out))
            print(f"wrote {args.out / 'index.html'} (exit {code}: "
                  f"{ {0: 'consistent', 1: 'differences need review', 2: 'incomplete or invalid'}[code] })")
            return code
        if args.command == "report":
            from . import report
            report.rerender(args.run, args.out, args.decisions)
            print(f"wrote {args.out / 'index.html'}")
            return 0
        if args.command == "verify-bundle":
            from . import report
            manifest = report.verify_bundle(args.run)
            print(f"ok: {len(manifest['files'])} files match the manifest; evidence {manifest['evidence_sha256']}")
            return 0
    except (contracts.ContractError, FileExistsError, FileNotFoundError) as exc:
        print(f"qref: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())

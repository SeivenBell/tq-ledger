#!/usr/bin/env bash
# Guided, real QRef demo for screen recording. Every step runs the actual command; nothing is replayed.
# Press Enter to advance. Usage: scripts/demo.sh   (from the repository root)
set -euo pipefail
cd "$(dirname "$0")/.."

REF=.qref/envs/reference/bin/python
TGT=.qref/envs/target/bin/python
STAMP=$(date -u +%H%M%S)
DIR=runs/demo-$STAMP

step() { printf '\n\033[1m%s\033[0m\n' "$1"; read -r -p "[Enter] " _; }
show() { printf '\033[2m$ %s\033[0m\n' "$*"; "$@"; }

step "1/5  Ask Claude to update the old code to Qiskit 2.x"
show uv run qref propose --case cases/qaoa.json --out "$DIR/proposal"
step "     What Claude says it changed"
sed -n '/## Intentional changes/,/## Uncertainties/p' "$DIR/proposal/notes.md" | sed '$d'

step "2/5  Run the old and new code side by side and compare what really happened"
set +e
show uv run qref run --case "$DIR/proposal/case.json" --reference-python "$REF" --target-python "$TGT" \
  --out "$DIR/run" --trust-local-code
echo "exit code: $?   (0 consistent, 1 differences need review, 2 incomplete or invalid)"
set -e

step "3/5  Open the report"
open "$DIR/run/index.html" 2>/dev/null || xdg-open "$DIR/run/index.html"

step "4/5  Record my decision"
reviewer=$(git config user.name || echo "Reviewer")
read -r -p "Decision (accepted_intentional / rejected / needs_review): " decision
read -r -p "Reason: " reason
uv run python - "$DIR" "$reviewer" "$decision" "$reason" <<'EOF'
import json, sys
from datetime import datetime, timezone
d, reviewer, decision, reason = sys.argv[1:]
t = json.load(open(f"{d}/run/review-template.json"))
now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
for entry in t["decisions"]:
    entry.update(decision=decision, reviewer=reviewer, reason=reason, recorded_at=now)
json.dump(t, open(f"{d}/review.json", "w"), indent=2)
print(f"wrote {d}/review.json ({len(t['decisions'])} finding(s))")
EOF
show uv run qref report --run "$DIR/run" --decisions "$DIR/review.json" --out "$DIR/reviewed"
open "$DIR/reviewed/index.html" 2>/dev/null || xdg-open "$DIR/reviewed/index.html"

step "5/5  Check that nothing in the report was changed"
show uv run qref verify-bundle --run "$DIR/reviewed"
cmp "$DIR/run/evidence.json" "$DIR/reviewed/evidence.json" && echo "evidence.json identical before and after the human decision"

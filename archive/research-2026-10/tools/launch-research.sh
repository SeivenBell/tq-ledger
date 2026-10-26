#!/usr/bin/env bash
# Start one Claude Code cloud session per Wayfinder research ticket.
# Usage: tools/launch-research.sh 3 4 5 ...   (issue numbers; defaults to the ten area tickets)
# Requires: `claude auth login`, GitHub connected for cloud sessions, environment network access set to Full.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

tickets=("$@")
[ ${#tickets[@]} -eq 0 ] && tickets=(3 4 5 6 7 8 9 10 11 12)

for n in "${tickets[@]}"; do
  title=$(gh issue view "$n" --json title -q .title)
  body=$(gh issue view "$n" --json body -q .body)
  IFS= read -r -d '' prompt <<EOF || true
You are resolving one Wayfinder research ticket for this repository.
Read CLAUDE.md and docs/wayfinder/research-brief.md first, then the existing reports in docs/research/.

Ticket #$n: $title

$body

Work as a careful research analyst: search the web, read primary sources in full, use subagents to read sources in parallel, and look for disconfirming evidence.
When done, write the report file named in the ticket, commit it on the branch named in the ticket, and push that branch. Do not open a pull request.
Finish by replying with the report's Bottom line section.
EOF
  echo "== launching ticket #$n: $title"
  claude --cloud "$prompt"
done

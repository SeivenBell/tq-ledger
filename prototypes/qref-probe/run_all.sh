#!/usr/bin/env bash
# Reproduce the QRef probe end to end.
set -u
cd "$(dirname "$0")"
[ -d legacy ] || { uv venv -p 3.11 legacy && uv pip install -p legacy "qiskit==0.46.3" "qiskit-aer==0.14.2" "qiskit-algorithms"; }
[ -d modern ] || { uv venv -p 3.13 modern && uv pip install -p modern "qiskit>=2,<3" "qiskit-aer"; }
mkdir -p traces
ports() {
  case $1 in
    s1_ghz) echo "port mut_postproc_endian mut_measure_map ok_other_seed" ;;
    s2_qaoa) echo "port port_fixed mut_rx_halfangle" ;;
    s3_teleport) echo "port mut_swapped_corrections ok_deferred_measurement ok_other_seed" ;;
  esac
}
for case in s1_ghz s2_qaoa s3_teleport; do
  for r in "" "--replay"; do
    sfx=${r:+.replay}
    legacy/bin/python qref/trace.py "traces/$case.legacy$sfx.json" "cases/$case/legacy.py" $r
    for p in $(ports $case); do
      modern/bin/python qref/trace.py "traces/$case.$p$sfx.json" "cases/$case/$p.py" $r
    done
  done
  for p in $(ports $case); do
    echo "=== $case / $p"
    modern/bin/python qref/compare.py "traces/$case.legacy.json" "traces/$case.$p.json" \
      "traces/$case.legacy.replay.json" "traces/$case.$p.replay.json"
  done
done

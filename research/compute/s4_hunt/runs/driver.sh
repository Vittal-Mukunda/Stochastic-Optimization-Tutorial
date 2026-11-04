#!/bin/bash
# sequential stages; each orbit_exh action is < 1h
cd "$(dirname "$0")/.."
while pgrep -f "run_actions.py 0 34" >/dev/null; do sleep 30; done
[ -f runs/FOUND_FLAG ] && exit 0
python3 run_actions.py 35 36 > runs/run_actions_35_36.out 2>&1
[ -f runs/FOUND_FLAG ] && exit 0
python3 run_actions.py 37 38 > runs/run_actions_37_38.out 2>&1
echo done > runs/driver.done

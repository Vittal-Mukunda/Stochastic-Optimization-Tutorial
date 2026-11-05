#!/bin/bash
# usage: run_cubes.sh n c solver timeout_seconds parallel outfile [index_list_file] [nos3]
# Runs every cube (or the indices listed one per line in index_list_file) with a wall-clock limit; one JSON line per cube.
n=$1; c=$2; solver=$3; tl=$4; par=$5; out=$6; idx=$7; extra=$8
here=$(cd "$(dirname "$0")" && pwd)
if [ -z "$idx" ] || [ "$idx" = "all" ]; then idx=$(mktemp); python3 "$here/p25_cube.py" list $n $c | awk '{print $1}' > "$idx"; fi
cat "$idx" | xargs -P "$par" -I{} bash -c '
  r=$(timeout '"$tl"' python3 '"$here"'/p25_cube.py solve '"$n $c"' {} '"$solver $extra"' 2>&1)
  if [ -z "$r" ]; then r="{\"n\": '"$n"', \"c\": '"$c"', \"index\": {}, \"result\": \"TIMEOUT\", \"solver\": \"'"$solver"'\", \"limit\": '"$tl"'}"; fi
  echo "$r" >> '"$out"'
'

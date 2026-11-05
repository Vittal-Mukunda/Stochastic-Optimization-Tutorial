#!/bin/bash
# usage: run_cubes_cpsat.sh n c time_limit workers outfile index_list_file [nos3]
# Runs the listed cubes one after another with CP-SAT (multi-worker portfolio); one JSON line per cube.
n=$1; c=$2; tl=$3; w=$4; out=$5; idx=$6; extra=$7
here=$(cd "$(dirname "$0")" && pwd)
while read -r i; do
  [ -z "$i" ] && continue
  r=$(timeout $(( ${tl%.*} + 120 )) python3 "$here/p25_cpsat.py" $n $c $i $tl $w $extra 2>&1 | tail -n 1)
  case "$r" in \{*) ;; *) r="{\"n\": $n, \"c\": $c, \"index\": $i, \"result\": \"ERROR\", \"solver\": \"cpsat\", \"msg\": \"$(echo $r | tr -d '\"' | head -c 200)\"}";; esac
  echo "$r" >> "$out"
done < "$idx"

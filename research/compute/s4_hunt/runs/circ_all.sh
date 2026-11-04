#!/bin/bash
cd "$(dirname "$0")"
for n in 65 63 61 59 57 55 53; do
  for j in 0 1 2 3; do ./circ_exh $n 4 $j 4 > circ_n${n}_j$j.out & done; wait
done
echo ALLDONE > circ_all.done

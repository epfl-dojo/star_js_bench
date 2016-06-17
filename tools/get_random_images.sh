#!/bin/bash
projDir="$(dirname $0)/.."
for stem in $(seq -w 00 09);   do
  (for stem2 in $(seq 0 9); do
    i="$stem$stem2";
    curl "http://lorempixel.com/index.php?generator=1&x=640&y=480&cat=" -o temp.html && cat temp.html | sed -n 's/.*<img src="\([^" ]*\)".*/\1/p' | awk '{print "http://lorempixel.com/"$1}' | xargs curl -o "${projDir}/data/images/$i.jpg";
  done) &
done

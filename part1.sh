#!/bin/bash

while read l; do
echo $l
grep "$l" dev.csv |\
tee "raw-$l.txt"|\
cut -d '#' -f 4 |\
tr -s '[:upper:]' '[:lower:]' |\
tr -d '[:punct:][:digit:]–…«' |\
tr -s '[:space:]' '\n' |\
grep -ivf stopwords.txt |\
sort |\
uniq -c |\
sort -n > "$l".txt
done < genre1.txt
#!/usr/bin/bash

# You need to change into the directory with ALL the results files & tell this script which week/round you are loading.
# This script will just produce gridding sheets from last week updated results.
# You could copy the previous weeks updated DB into the right Week, before running this

# Set PATH to include binary
$PATH=$PATH:../bin

mkdir gridding 2>/dev/null

# Now produce gridding sheets in CSV and move them to the "gridding" directory so I can find them!
for f in U8.db U10.db U12.db Youth.db Women.db Senior.db Vet50.db
do
  echo "Producing gridding files for $f"
  dump_gridding_order.py $f
  mv $f-gridding.csv gridding
done



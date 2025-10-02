#!/usr/bin/bash

# You need to change into the directory with ALL the results files & tell this script which week/round you are loading.

# Set PATH to include binary
PATH=$PATH:../bin

mkdir gridding 2>/dev/null

# Check we have the results files:
for f in Senior-results.csv
do
	if [ ! -f ${f} ] ; then
		echo "Cannot fopen CSV file $f. Exiting"
		exit 5
	fi
done

# Check we have the database files for each race:
for f in Senior.db
do
	if [ ! -f ${f} ] ; then
		echo "Cannot open DB file $f. Exiting"
		exit 5
	fi
done

# Check we have a week/round!
if [ $# -lt 1 ]; then
    echo "Usage: $0 <num> # Where num is the round number - between 1 and 12"
    exit 1
fi

Week=$1


# Take each filtered input file and produce category ranking

# Senior race
for f in Senior-results.csv
do
  echo "Updating $f filtering DNFs & non-league riders & re-ranking for Junior, Senior, U23 and M40"
  # Strip binaries
  remove_bins.py $f

  # Remove non league & DNFs
  filter_results.py $f -o modified${f}

  egrep "^Pos|,Junior," modified${f} > J-${f}
  egrep "^Pos|,Senior,|,Under 23," modified${f} > S-${f}
#  egrep "^Pos|,Under 23," modified${f} > U-${f}
  egrep "^Pos|,M 40-49," modified${f} > V40-${f}
  
  # Now re-rank each category - This will produce "modifed" file.
  for f in J-${f} V40-${f}
  do
    echo "Updating $f filtering category for Junior, Senior, U23 and M40"
    echo filter_results_category.py $f
    filter_results_category.py $f
  done
done
filter_results.py S-Senior-results.csv -o modifiedS-Senior-results.csv


# Now we can load the CSV files into databases:

# Senior (Junior, U23s, V40's)
for f in J-Senior-results.csv V40-Senior-results.csv
do
  load_race_results.py Senior.db modified_${f} $Week
done
load_race_results_senior.py Senior.db modifiedS-Senior-results.csv $Week

# Last step is to update each database with average positions & race counts and points.
for f in Senior.db 
do
  echo "Updating $f with Race info & average position"
  # Once loaded, update the races finished (just needed for information):
  update_race_count.py $f

  # Now update their points total:
  update_riders_race_points.py $f $Week

  # Once race points are updated, calculate the riders total AND update their best 10 (note to change update sciprt)
  update_race_points.py $f

  # This should allow us to update the average position - needed for gridding
  update_average.py $f

done


# Final stage is to produce the CSVs for the spreadsheet...

# Junior Male
produce_league_tables-singlecat.py Senior.db JunM

# V40
produce_league_tables-dualcat.py Senior.db M40M M45M

# Senior
produce_league_tables-dualcat.py Senior.db "SenM" "U23M"


mkdir LEAGUE_TABLES 2>/dev/null
mv *leaguetable.csv LEAGUE_TABLES

mv S-Senior-results.csv league-workingfiles
mv J-Senior-results V40-Senior-results.csv league-workingfiles


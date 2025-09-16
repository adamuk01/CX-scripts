#!/usr/bin/bash

# You need to change into the directory with ALL the results files & tell this script which week/round you are loading.

# Set PATH to include binary
PATH=$PATH:../bin

# Check we have the results files:
for f in Women-results.csv
do
	if [ ! -f ${f} ] ; then
		echo "Cannot fopen CSV file $f. Exiting"
		exit 5
	fi
done

# Check we have the database files for each race:
for f in Women.db
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

# Women - No seperate categories here
for f in Women-results.csv 
do
  echo "Updating $f filtering DNFs & non-league riders & re-ranking"
  # Strip binaries
  remove_bins.py $f

  # Remove non league & DNFs
  filter_results.py $f -o modified${f}
done



# Now we can load the CSV files into databases:

# Women race
for f in Women-results.csv
do
  load_race_results.py Women.db modified${f} $Week
done


# Last step is to update each database with average positions & race counts and points.
for f in Women.db
do
  echo "Updating $f with Race info & average position"
  # Once loaded, update the races finished (just needed for information):
  update_race_count.py $f

  # Calculate the number of points for each rider:
  update_riders_race_points-womenonly.py $f $Week

  # Once race points are updated, calculate the riders total AND update their best 10 (note to change update sciprt)
  update_race_points.py $f

  # This should allow us to update the average position - needed for gridding
  update_average.py $f

done

# Final stage is to produce the CSVs for the spreadsheet...
# Women
produce_league_tables-singlecat.py Women.db "%"

mv %-leaguetable.csv Women-leaguetable.csv

mkdir LEAGUE_TABLES
mv *leaguetable.csv LEAGUE_TABLES

mkdir league-workingfiles
mv modified_*.csv league-workingfiles

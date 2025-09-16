#!/usr/bin/bash

# You need to change into the directory with ALL the results files & tell this script which week/round you are loading.

# Set PATH to include binary
PATH=$PATH:../bin

# Check we have the results files:
for f in U8-results.csv 
do
	if [ ! -f ${f} ] ; then
		echo "Cannot open CSV file $f. Exiting"
		exit 5
	fi
done

# Check we have the database files for each race:
for f in U8.db 
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

# U8's - Make & Female & U6 and U8
for f in U8-results.csv 
do
  echo "Updating $f filtering DNFs & non-league riders & re-ranking"
  # Strip binaries
  remove_bins.py $f

  # Remove non league & DNFS
  filter_results.py $f -o modified${f}

  egrep "^Pos|Under 8" modified${f} | egrep "^Pos|,Female," > F-U8.csv
  egrep "^Pos|Under 6" modified${f} | egrep "^Pos|,Female," > F-U6.csv

  egrep "^Pos|Under 8" modified${f} | egrep "^Pos|,Male," > M-U8.csv
  egrep "^Pos|Under 6" modified${f} | egrep "^Pos|,Male," > M-U6.csv
  
  # Now re-rank each category - This will produce "modifed" file.
  for f in F-U8.csv F-U6.csv M-U8.csv M-U6.csv
  do
    filter_results_category.py $f
  done
done


# Now we can load the CSV files into databases:

# U8's
for f in F-U8.csv F-U6.csv M-U8.csv M-U6.csv
do
  echo $f has `wc -l modified_${f}` lines
  load_race_results.py U8.db modified_${f} $Week
done


# Last step is to update each database with average positions & race counts and points.
for f in U8.db 
do
  echo "Updating $f with Race info & average position"
  # Once loaded, update the races finished (just needed for information):
  update_race_count.py $f

  # Calculate the number of points for each rider, based on category:
  update_riders_race_points.py $f $Week

  # Once race points are updated, calculate the riders total AND update their best 10 (note to change update sciprt)
  update_race_points.py $f

  # This should allow us to update the average position - needed for gridding
  update_average.py $f

done

# Now produce league tables
# U6 + U8
# produce_points_csv.py <DB_FILE> <CATEGORY>
produce_league_tables-singlecat.py U8.db U6F
produce_league_tables-singlecat.py U8.db U6M
produce_league_tables-singlecat.py U8.db U8F
produce_league_tables-singlecat.py U8.db U8M


mkdir LEAGUE_TABLES
mv *leaguetable.csv LEAGUE_TABLES

mkdir league-workingfiles
mv modified*.csv league-workingfiles


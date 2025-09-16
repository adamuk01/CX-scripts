#!/usr/bin/bash
#
trap 'read -p "Press Enter to run: $BASH_COMMAND"' DEBUG

# You need to change into the directory with ALL the results files & tell this script which week/round you are loading.

# Set PATH to include binary
PATH=$PATH:../bin

mkdir gridding 2>/dev/null

# Check we have the results files:
for f in Vet50-results.csv
do
	if [ ! -f ${f} ] ; then
		echo "Cannot fopen CSV file $f. Exiting"
		exit 5
	fi
done

# Check we have the database files for each race:
for f in Vet50.db
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
# Vet50 & Vet60 Men
for f in Vet50-results.csv
do
  echo "Updating $f filtering DNFs & non-league riders & re-ranking for Masters 50 and Masters 60 category"
  # Strip binaries
  remove_bins.py $f

  # Remove non league & DNFs
  filter_results.py $f

  egrep "^Pos|,M 50-59," modified${f} > V50-${f}
  egrep "^Pos|,M 60\+," modified${f} > V60-${f}
  
  # Now re-rank each category - This will produce "modifed" file.
  for f in V50-${f} V60-${f}
  do
    filter_results_category.py ${f}
  done
done


# Now we can load the CSV files into databases:

# Vet50 race/DB
for f in V50-Vet50-results.csv V60-Vet50-results.csv
do
  load_race_results.py Vet50.db modified_${f} $Week
done



# Last step is to update each database with average positions & race counts and points.
for f in Vet50.db
do
  echo "Updating $f with Race info & average position"
  # Once loaded, update the races finished (just needed for information):
  update_race_count.py $f

  # Calculate the number of points for each rider:
  update_riders_race_points.py $f $Week

  # Once race points are updated, calculate the riders total AND update their best 10 (note to change update sciprt)
  update_race_points.py $f

  # This should allow us to update the average position - needed for gridding
  update_average.py $f
done


# Final stage is to produce the CSVs for the spreadsheet...
# Vet 50 
produce_league_tables-dualcat.py Vet50.db M50M M55M

# Vet 60 
produce_league_tables-dualcat.py Vet50.db "M60" "M65"

# Vet 70 
produce_league_tables-dualcat.py Vet50.db "M70" "M75"

mkdir LEAGUE_TABLES
mv *leaguetable.csv LEAGUE_TABLES

mkdir league-workingfiles
mv modified*.csv league-workingfiles

#!/usr/bin/bash

# You need to change into the directory with ALL the current database files 

# Set PATH to include binary
PATH=$PATH:../bin

mkdir teamawards 2>/dev/null


# Check we have the database files for each race:
for f in Senior.db U10.db  U12.db  U8.db  Vet50.db  Women.db  Youth.db
do
	if [ ! -f ${f} ] ; then
		echo "Cannot open DB file $f. Exiting"
		exit 5
	fi
done

echo Merging databases...
merge_youth_databases.py
merge_adult_databases.py
merge_databases.py

echo Moving new databases to teamawrds directory
mv U12RidersMerged.db AdultRidersMerged.db AllRidersMerged.db teamawards

cd teamawards

# Remove average points - which are 999
echo "Removing any average points markers"
echo "U12RidersMerged.db"
set_999_averagepoints_to_zero.py U12RidersMerged.db
echo "AdultRidersMerged.db"
set_999_averagepoints_to_zero.py AdultRidersMerged.db
echo "AllRidersMerged.db"
set_999_averagepoints_to_zero.py AllRidersMerged.db

echo Running Participation Award for the Mick Ives Trophy
# This is the Participation Award for the Mick Ives Trophy
../../bin/count_club_races.py AllRidersMerged.db > RidersTotalRaces.csv

echo Running TEAM COMPETITION - Highest scoring 6 riders from each club
# TEAM COMPETITION - Highest scoring 6 riders from each club to score each round 
echo "Position,Team,Points" > TeamCompetition-Kids.csv
echo "Position,Team,Points" > TeamCompetition-Adults.csv
../../bin/produce_team_winners4.py U12RidersMerged.db |  sed 's/[][\/$*.^|@#{}~&()_:;%+"='\'',`><?!-]/ /g' | sed 's/  /,/g' | grep -v ",No Club Team" >> TeamCompetition-Kids.csv
../../bin/produce_team_winners4.py AdultRidersMerged.db | sed 's/[][\/$*.^|@#{}~&()_:;%+"='\'',`><?!-]/ /g' | sed 's/  /,/g' | grep -v ",No Club Team" >> TeamCompetition-Adults.csv



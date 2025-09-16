#!/usr/bin/bash

# You need to change into the directory with ALL the results files & tell this script which week/round you are loading.

# Set PATH to include binary
$PATH=$PATH:../bin

mkdir gridding 2>/dev/null

# Check we have the results files:
for f in U8-results.csv U10-results.csv U12-results.csv Youth-results.csv Women-results.csv Senior-results.csv Vet50-results.csv
do
	if [ ! -f ${f} ] ; then
		echo "Cannot fopen CSV file $f. Exiting"
		exit 5
	fi
done

# Check we have the database files for each race:
for f in U8.db U10.db U12.db Youth.DB Women.db Senior.db Vet50.db
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
  filter_results.py $f

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

# U10's - just Male and Female
for f in U10-results.csv 
do
  echo "Updating $f filtering DNFs & non-league riders & re-ranking"
  # Strip binaries
  remove_bins.py $f

  # Remove non league & DNFS
  filter_results.py $f

  egrep "^Pos|Under 10" modified${f} | egrep "^Pos|,Female," > F-${f}
  egrep "^Pos|Under 10" modified${f} | egrep "^Pos|,Male," > M-${f}
  
  # Now re-rank each category - This will produce "modifed" file.
  for f in F-${f} M-${f}
  do
    filter_results_category.py $f
  done
done

# U12's - just Male and Female
for f in U12-results.csv 
do
  echo "Updating $f filtering DNFs & non-league riders & re-ranking"
  # Strip binaries
  remove_bins.py $f

  # Remove non league & DNFS
  filter_results.py $f

  egrep "^Pos|Under 12" modified${f} | egrep "^Pos|,Female," > F-${f}
  egrep "^Pos|Under 12" modified${f} | egrep "^Pos|,Male," > M-${f}
  
  # Now re-rank each category - This will produce "modifed" file.
  for f in F-${f} M-${f}
  do
    filter_results_category.py $f
  done
done


# Youth's - Male and Female U14 and U16
for f in Youth-results.csv 
do
  echo "Updating $f filtering DNFs & non-league riders & re-ranking"
  # Strip binaries
  remove_bins.py $f

  # Remove non league & DNFS
  filter_results.py $f

  egrep "^Pos|,Youth A," modified${f} | egrep "^Pos|,Female," > F-YA.csv
  egrep "^Pos|,Youth A," modified${f} | egrep "^Pos|,Male," > M-YA.csv

  egrep "^Pos|,Youth B," modified${f} | egrep "^Pos|,Female," > F-YB.csv
  egrep "^Pos|,Youth B," modified${f} | egrep "^Pos|,Male," > M-YB.csv
  
  # Now re-rank each category - This will produce "modifed" file.
  for f in F-YA.csv M-YA.csv F-YB.csv M-YB.csv
  do
    filter_results_category.py $f
  done
done


# Women - No seperate categories here
for f in Women-results.csv 
do
  echo "Updating $f filtering DNFs & non-league riders & re-ranking"
  # Strip binaries
  remove_bins.py $f

  # Remove non league & DNFs
  filter_results.py $f
done


# Senior race
for f in Senior-results.csv
do
  echo "Updating $f filtering DNFs & non-league riders & re-ranking for Junior, Senior, U23 and Vet40"
  # Strip binaries
  remove_bins.py $f

  # Remove non league & DNFs
  filter_results.py $f

  egrep "^Pos|,Junior," modified${f} > J-${f}
  egrep "^Pos|,Senior,|,Under 23," modified${f} > S-${f}
  egrep "^Pos|,Vet 40-49," modified${f} > V40-${f}
  
  # Now re-rank each category - This will produce "modifed" file.
  for f in J-${f} S-${f} V40-${f}
  do
    filter_results_category.py $f
  done
done


# Vet50 & Vet60 Men
for f in Vet50-results.csv
do
  echo "Updating $f filtering DNFs & non-league riders & re-ranking for Vet 50 and Vet60 category"
  # Strip binaries
  remove_bins.py $f

  # Remove non league & DNFs
  filter_results.py $f

  egrep "^Pos|,Vet 50-59," modified${f} > V50-${f}
  egrep "^Pos|,Vet 60+," modified${f} > V60-${f}
  
  # Now re-rank each category - This will produce "modifed" file.
  for f in V50-${f} V60-${f}
  do
    filter_results_category.py V50-${f}
  done
done


# Now we can load the CSV files into databases:

# U8's
for f in F-U8.csv F-U6.csv M-U8.csv M-U6.csv
do
  load_race_results.py U8.db modified_${f} $week
done

# U10's
for f in F-U10.csv M-U10.csv
do
  load_race_results.py U10.db modified_${f} $week
done


# U12's
for f in F-U12.csv F-U12.csv M-U12.csv M-U12.csv
do
  load_race_results.py U12.db modified_${f} $week
done

# Youth
for f in F-YA.csv F-YB.csv M-YA.csv M-YB.csv
do
  load_race_results.py Youth.db modified_${f} $week
done

# Women race
for f in Women-results.csv
do
  load_race_results.py Women.db modified${f} $week
done


# Senior (Junior, U23s, V40's)
for f in J-Senior-results.csv S-Senior-results.csv  V40-Senior-results.csv
do
  load_race_results.py Senior.db modified_${f} $week
done


# Vet50 race/DB
for f in V50-Vet50-results.csv V60-Vet60-results.csv
do
  load_race_results.py Vet50.db modified_${f} $week
done



# Last step is to update each database with average positions & race counts and points.
for f in U8.db U10.db U12.db Youth.db Women.db Senior.db Vet40.db Vet50.sb Vet60.db
do
  echo "Updating $f with Race info & average position"
  # Once loaded, update the races finished (just needed for information):
  update_race_count.py $f

  # This should allow us to update the average position - needed for gridding
  update_average.py $f

  # Calculate the number of points for each rider:

  # Now update their points total:
  if [ "$f" == "Women.db" ] ; then
    calculate_race_points-womenonly.py $f $Week
  else
    calculate_race_points.py $f $Week
  fi

  # Once race points are updated, calculate the riders total AND update their best 10 (note to change update sciprt)
  update_race_points.py $f

done


# Final stage is to produce the CSVs for the spreadsheet...

# U6 + U8
# produce_points_csv.py <DB_FILE> <CATEGORY>
produce_league_tables.py U8.db "Under 8"
produce_league_tables.py U8.db "Under 6"

# U10
produce_league_tables.py U10.db "Under 10"

# U12
produce_league_tables.py U12.db "Under 12"

# Youth
produce_league_tables.py Youth.db "Youth A"
produce_league_tables.py Youth.db "Youth B"

# Women
produce_league_tables.py Women.db "%"
rm -f %-Male-leaguetable.csv
mv %-Female-leaguetable.csv Women-Female-leaguetable.csv

# Junior Male
produce_league_tables.py Senior.db "Junior"
rm -f Junior-Female-leaguetable.csv

# Senior
produce_league_tables.py Senior.db "Senior"
rm -f Senior-Female-leaguetable.csv

# Vet 40
produce_league_tables.py Senior.db "Vet 40-49"

# Vet 50 
produce_league_tables.py Vet50.db "Vet 50-59"

# Vet 60 
produce_league_tables.py Vet50.db "Vet 60+"
rm -f Vet*Female-leaguetable.csv

mkdir LEAGUE_TABLES
mv *leaguetable.csv LEAGUE_TABLES


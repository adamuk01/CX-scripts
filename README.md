Start Sheets are a manual process. Gridding produced on back of it.

Gridding & start sheets is a multi phase process. It needs the league tables to be upto date from the previous weeks race. Otherwise we are not sure where the league riders will go.

We also need to get the RiderHQ file and process that.

First validate it - by hand and fix anything:

Put it in the right round we are running next and call it: WMCCLRiderEntry.csv

validate_csv_report.py WMCCLRiderEntry.csv
validate_csv.py WMCCLRiderEntry.csv
validate_csv_spaces.py WMCCLRiderEntry.csv

This checks for errors in file from Organiser.

Now sort it and allocate number to non-league riders:

produce_start-sheet.py corrected_WMCCLRiderEntry.csv allRiders.csv

produce_sorted_csv-start-list.py allRiders.csv

produce_category_from_riderHQ.py allRiders.csv allRiders+cat.csv 
validate_csv_against_db.py XXXXX.db allRiders.csv <- each database!

Run the summary script on it - to check for numbers. This does not check the category!
summerise-riders.sh allRiders+cat.csv

Validate the race numbers match in CSV file & DB:
validate_category_by_race_number.py WMCCLRiderEntry.csv
validate_race_numbers.sh


Now copy the file to StartList.csv and run the script to detect if they are 1 bike or not:
cp allRiders.csv StartList.csv
add_1BX_to_allRiderscsv.py StartList.csv


Start sheets

Check the output… Make sure we have ALL the right riders. 
This file “StartList.csv” will be used to produce start sheets! 

Do this by hand - copying & pasting data in. Then make sure you sort the data by Sex, then Surname in certain categories! Send organiser the PDF.

Gridding sheets

Edit the file raceheader.txt which is in the Week directory. This just prints a header of date/location at the top of each sheet.

From here on it rest can be automated using “produce-gridding-sheets.sh” - For info/notes it calls:
NOTE: Edit this script first few weeks so it does NOT chop the last fields! Last years average.


produce_gridding_order.py file.db
	This gives a file with ALL the league riders gridding position. Based on the database you pass it.
	We get one for each race.

produce_league_members_grid.py Women.db-gridding.csv Women-gridding.csv allriders.csv
	This takes the file produced in the first step (all league gridding) - uses the processed riderHQ file 		(allriders.csv). It outputs a CSV file, in the example: Women-gridding.csv which has the league 			riders ranked.

Next step is to add the non-league members to the end.

filter_non-league_riders_from_csv.py allriders | grep CATEGORY >> gridding_file

e.g

filter_non-league_riders_from_csv.py allriders.csv | egrep "Junior Female|Female 18+">> Women.db-gridding.csv

Final stage is to normalise the Position in the file:

update_csv_position.py CSV_FILE

e.g

update_csv_position.py Women.db-gridding.csv

now have a CSV file for each race. Convert to PDF and send them to organiser.

Send along with start-sheets spreadsheet.After race need to update the databases with the results:

Get the CSV results files from Mick. All them the category + -results.csv

These need to be put in the Week/Round directory, with the DB files which should already be there (to produce gridding & start sheets).

Now run : run-ALL-race-update.sh [Round-number]

Or run each script with the round number. In the right week/round directory:

run-U8-race-update.sh
run-U10-race-update.sh
run-U12-race-update.sh
run-Youth-race-update.sh
run-Women-race-update.sh
run-Senior-race-update.sh
run-Vet50-race-update.sh

Each run will - remove any binary chars, remove non-league riders (race number > 870) and DNFs. Then it re-orders the riders final race position. If necessary, update their category position next. Then load into database.
Now we can update race count, riders race points, Rider total race points and best 10 results. Finally update their average (needed for gridding).
Then output the CSV files for the league tables.
The data has to be copied into empty lease table spreadsheets, to the output in PDF format for the web site.


Participation award:

run-team-awards-results.sh

Output will be in “teamawards” subdirectory

Average points allocation

This changes their round points to 999 - need to change this is spreadsheet to “AP”.
You MUST run this AFTER working out results (otherwise the 999 value will be removed!)

Run allocate_average_points.py to allocate average points. e.g:

allocate_average_points.py Women.db 651 6

Give rider 651 average points (999) for round 6. It will display name and prompt for verification.

When calculating team awards these 999 values must be removed. So script set_999_averagepoints_to_zero.py does this to the merged databases.

At the end of the season, the 999 values MUST be replaced with actual average points. This is done via convert_999_to_average.py script
e.g
convert_999_to_average.py Senior.db

Make sure to copy the databases to new directory first! Just in case…Creating databases in the first place.

All work should be done in /nas/CX/Initial-load
Should be “LastYearsRiders.csv” file. Containing key data from last years riders (see section below to create).

Need to create databases for each of the 5 races:
create_dbs.sh

Now we need to validate data from RiderHQ file: RiderHQInitialData.csv
This should have all rider data with race numbers in it.

Check for blank fields, duplicate lines & names: 
validate_csv.py RiderHQInitialData.csv
validate_csv_spaces.py RiderHQInitialData.csv

Validate spaces will correct fields and output new file.

Now we have to split out each category to load into correct DB

Load the data into the database:
At the moment this script will need changing! Not sure the order of the CSV file from RiderHQ:
import_rider_data.py U8.db U8.csv
Each file should just container riders in each race.

Check to see if the rider rode last year, IF so we need from CSV file LastYearsRiders.csv

initial-load-import-last-years-data.py U8.db LastYearsRiders.csv

Give it the database & the same CSV file. Need to run on each database, against same CSV file.

Now have to set the race_category_current_year to a valid value:

First check the script - make sure years match! 
update_riders_category_current_year.py should be updated every year.

update_riders_category_current_year.py U8.db

Now need to check IF they have changed category. If they have update “race_category_update” to Y
If race_category_update is “Y”, we need to adjust their average_position_last_year:

If U8, U12, Youth take away 10 points from average_position_last_year. 

If V4* or V5* or V6*  add 5 

initial-load-check-category.py U8.db

At the moment this just takes 10 away - but can easily be changed to add 5 on.. code is there.

Fix the club names for “Another club”:

fix-club-name.py corrected_RiderHQInitialData.csv Senior.db

Verification.

Compare CSV file to database : 
for f in *.db; do echo $f; count_records.py $f; done
Compare against each CSV file : wc -l U*.csv Women.csv Youth.csv Vet50.csv
Check each database by hand, if they had category last year, do they have average points for last year - they should have!Adding more riders to database after first race

Repeat above procedure with smaller CSV file of the new riders the initial creation. Then rename each database “newriders-RACE.db”

Once the database looks fine, with rider history etc, merge it into existing database:

merge_two_databases.py Vet50.db newriders-Vet50.db


Creating LastYearsRiders.csv in the first place.

All work should be done in /nas/CX/Initial-load
Merge the FINAL results into a single DB file using merge_databases.py and put in Initial-load directory.

The dump this database to CSV using dump_db.py AllRidersMerged.db  AllRiders.csv

Edit the file in spreadsheet removing columns not required and renaming a couple.
Should be:

id      BC_number       race_number     First name      Last name       gender  club_name       race_category_current_year      DOB     YOB     IBX     average_position        races_finished  total_points    average_points

Actually only need:

firstname = row['First name']
surname = row['Last name']
YOB = row[‘YOB']
race_category_current_year = row['race_category_current_year']
races_finished = row['races_finished']
total_points = row['total_points']
average_position = row['average_position']
average_points = row['average_points']

File should be called LastYearsRiders.csv

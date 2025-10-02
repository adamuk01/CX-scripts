#!/usr/bin/bash

# You need to change into the directory with ALL the database files & the RiderHQ file - which has been manually checked & filtered!
# Should be run form the WeekX directory
# Filtered RiderHQ file - called "allRiders.csv" should be present
# Remove the chop last field line if on weeks 1 or 2.

# Set PATH to include binary
PATH=$PATH:../bin
riderHQfile=allRiders.csv
riderHQfilecat=allRiders+cat.csv

mkdir gridding 2>/dev/null

# Check we have the database files for each race:
for f in U8.db U10.db U12.db Youth.db Women.db Senior.db Vet50.db
do
	if [ ! -f ${f} ] ; then
		echo "Cannot open DB file $f. Exiting"
		exit 5
	fi
done

if [ ! -f $riderHQfile ] ; then
	echo "Cannot open CSV file from riderHQ $riderHQfile"
	exit 5
fi

# This will add a category onto the riderHQ file. It is needed for Kids races where U6/U8 are gridded after each other
produce_category_from_riderHQ.py $riderHQfile $riderHQfilecat.tmp

# Ths will correct the member to true/fales based on their rider number
validate_members_by_racenumber.py $riderHQfilecat.tmp $riderHQfilecat
rm -f $riderHQfilecat.tmp


for f in *.db
do
	produce_gridding_order.py $f
	# This will produce $f-gridding.csv - now need to filter the riders as to who has actually entered
	# Or do we ? What if they entered on the day ? 
	# Maybe we should just filter on riders who have zero races and zero ranking last year?
done

mv *gridding.csv gridding
cp $riderHQfile gridding
cp $riderHQfilecat gridding
cd gridding

echo "Moving into Gridding, finding League Members"

for f in U*.csv Y*.csv W*.csv S*.csv V*.csv
do
	newfile=`basename $f`
	produce_league_members_grid.py $f ${newfile}-league.csv $riderHQfile
	# This will generate file with our riders - minus non-league riders. Now need to add them...
done

#
#

# Now find non-league riders, They should have "Has membership" set to FALSE
# U8/U10

echo "Finding non-League Members"
strings $riderHQfilecat | egrep "^Under 8" | grep FALSE | awk -F, '{print "200,"$3,$4","$14","$10","$15","$8",,"}' >> U8.db-gridding-nonleague.csv

strings $riderHQfilecat | egrep "^Under 10" | grep FALSE | awk -F, '{print "200,"$3,$4","$14","$10","$15","$8",,"}'  >> U10.db-gridding-nonleague.csv

# U12
strings $riderHQfilecat | egrep "^Under 12" | grep FALSE | awk -F, '{print "200,"$3,$4","$14","$10","$15","$8","}' >> U12.db-gridding-nonleague.csv

# Youth
strings $riderHQfilecat | egrep "^Youth" | grep FALSE | awk -F, '{print "200,"$3,$4","$14","$10","$15","$8",,"}' >> Youth.db-gridding-nonleague.csv

# Vet50+
strings $riderHQfilecat | egrep "^Masters 50+" | grep FALSE | awk -F, '{print "200,"$3,$4","$14","$10","$15"M,"$8","}' >> Vet50.db-gridding-nonleague.csv

# Women
strings $riderHQfilecat | egrep "^Senior/Masters Female|^Junior Female" | grep FALSE | awk -F, '{print "200,"$3,$4","$14","$10","$15","$8","}' >> Women.db-gridding-nonleague.csv

# Seniors + Vet40 + Junior Men
strings $riderHQfilecat | egrep "^Masters 40|Senior Open|Junior Male" | grep FALSE | awk -F, '{print "200,"$3,$4","$14","$10","$15","$8","}' >> Senior.db-gridding-nonleague.csv

# We now have csv files for ALL our riders, all our riders who have entered & non-league riders. We need to combine these.
#
#
#
echo "Merging league & non-league members"
for f in U8 U10 U12 Youth 
do
	cat $f.db-gridding.csv-league.csv $f.db-gridding-nonleague.csv > Race-$f.csv
	# Now remove the last field - Last years average from the file. Only do this after week 2 or 3.
	#chop-last-field-csv.py Race-$f.csv
done


for f in Women Vet50 Senior
do
	cat $f.db-gridding.csv-league.csv > Race-$f.csv
	cat $f.db-gridding-nonleague.csv >> Race-$f.csv
	# Now remove the last field - Last years average from the file. Only do this after week 2 or 3.
	#chop-last-field-csv.py Race-$f.csv
done

# Remove any annoying team names...
for f in Race-*.csv
do
	echo "Filtering $f for annoying team names"
	sed -i 's/Team Mi Racing Townsend Vehicle Hire/Team Mi Racing/g' $f
done

# Show me a summary!
echo ====================
for f in Race*.csv
do
	echo "Lines in $f `grep '^[0-9]' $f | wc -l` "
done

# We have the race list, now we must for some of them to split the geners plus race cats (only for some!)
#
echo "Splitting races by age & gender"
# U8
egrep "Pos" Race-U8.csv > Final-U8.csv
echo ",U8 FEMALE" >> Final-U8.csv
egrep "U8" Race-U8.csv | grep Female >> Final-U8.csv
egrep "Under-8" Race-U8.csv | grep Female >> Final-U8.csv
echo ",ANY OTHER U8 FEMALE" >> Final-U8.csv
echo "," >> Final-U8.csv
echo ",U8 MALE" >> Final-U8.csv
egrep "U8" Race-U8.csv | grep Male >> Final-U8.csv
egrep "Under-8" Race-U8.csv | grep Male >> Final-U8.csv
echo ",ANY OTHER U8 NOT CALLED" >> Final-U8.csv
echo "," >> Final-U8.csv
echo ",UNDER 6 RIDERS" >> Final-U8.csv
egrep "U6" Race-U8.csv | grep Female >> Final-U8.csv
egrep "Under-6" Race-U8.csv | grep Female >> Final-U8.csv
echo ",ANY OTHER U6 FEMALE" >> Final-U8.csv
echo "," >> Final-U8.csv
egrep "U6" Race-U8.csv | grep Male >> Final-U8.csv
egrep "Under-6" Race-U8.csv | grep Male >> Final-U8.csv
echo ",ANY OTHER U6" >> Final-U8.csv

# U10
egrep "Pos" Race-U10.csv > Final-U10.csv
echo ",U10 FEMALE" >> Final-U10.csv
egrep "U10" Race-U10.csv | grep Female >> Final-U10.csv
egrep "Under-10" Race-U10.csv | grep Female >> Final-U10.csv
echo ",ANY OTHER U10 FEMALE" >> Final-U10.csv
echo "," >> Final-U10.csv
echo ",U10 MALE" >> Final-U10.csv
egrep "U10" Race-U10.csv | grep Male >> Final-U10.csv
egrep "Under-10" Race-U10.csv | grep Male >> Final-U10.csv
echo ",ANY OTHER U10" >> Final-U10.csv

# U12
egrep "Pos" Race-U12.csv  > Final-U12.csv
echo ",U12 FEMALE" >> Final-U12.csv
cat Race-U12.csv | grep Female >> Final-U12.csv
echo ",ANY OTHER U12 FEMALE" >> Final-U12.csv
echo "," >> Final-U12.csv
echo ",U12 MALE" >> Final-U12.csv
cat Race-U12.csv | grep Male >> Final-U12.csv

# Youth
egrep "Pos" Race-Youth.csv > Final-Youth.csv
echo ",U16 MALE" >> Final-Youth.csv
egrep "U16" Race-Youth.csv | grep Male >> Final-Youth.csv
egrep "Under-16" Race-Youth.csv | grep Male >> Final-Youth.csv
echo ",ANY OTHER U16 MALE" >> Final-Youth.csv
echo "," >> Final-Youth.csv
echo ",U14 MALE RIDERS" >> Final-Youth.csv
egrep "U14" Race-Youth.csv | grep Male >> Final-Youth.csv
egrep "Under-14" Race-Youth.csv | grep Male >> Final-Youth.csv
echo ",ANY OTHER U14 MALE" >> Final-Youth.csv
echo "," >> Final-Youth.csv
echo ",U16/U14 FEMALE RIDERS" >> Final-Youth.csv
egrep "U16" Race-Youth.csv | grep Female >> Final-Youth.csv
egrep "Under-16" Race-Youth.csv | grep Female >> Final-Youth.csv
echo ",ANY OTHER U16 FEMALE" >> Final-Youth.csv
echo "," >> Final-Youth.csv
egrep "U14" Race-Youth.csv | grep Female >> Final-Youth.csv
egrep "Under-14" Race-Youth.csv | grep Female >> Final-Youth.csv
echo ",ANY OTHER U14 FEMALE" >> Final-Youth.csv

# Women
cat Race-Women.csv > Final-Womens.csv

# Senior
egrep "Pos" Race-Senior.csv > Final-Senior.csv
echo ",JUNIOR RIDERS" >> Final-Senior.csv
egrep ",Jun" Race-Senior.csv >> Final-Senior.csv
echo ",ANY OTHER JUNIOR RIDER!" >> Final-Senior.csv
echo "," >> Final-Senior.csv
echo ",SENIOR/U23 RIDERS" >> Final-Senior.csv
egrep "Senior|Under-23|SenM|U23M|Unknown" Race-Senior.csv >> Final-Senior.csv
echo ",ANY OTHER U23/SENIOR RIDER!" >> Final-Senior.csv
echo "," >> Final-Senior.csv
echo ",M40 RIDERS" >> Final-Senior.csv
egrep ",M4." Race-Senior.csv >> Final-Senior.csv


# Vet50
egrep "Pos" Race-Vet50.csv > Final-Vet50.csv
echo ",M50 RIDERS" >> Final-Vet50.csv
egrep "M5.M|Masters 5" Race-Vet50.csv >> Final-Vet50.csv
echo ",ANY OTHER M50 RIDER!" >> Final-Vet50.csv
echo "," >> Final-Vet50.csv
echo ",M60+ RIDERS" >> Final-Vet50.csv
egrep "M6.M|M7.M|Masters 6|Masters 7" Race-Vet50.csv >> Final-Vet50.csv

#
#
#
# Now we can create the gridding sheets in PDF format:
#
echo "Creating PDFs"
for f in Final*
do
	echo $f
	# Normalise the positions:
	update_csv_position.py $f

	# Add a line for other riders that enter on the day
	echo ",ANY RIDER NOT CALLED" >> $f

	# Covert to PDF and add a header to the file
	cat=`echo $f | cut -d\. -f1 | cut -d- -f2`
	cat=$cat" Gridding. `cat ../raceheader.txt`"
	pdfoutput=`basename $f .csv`
	convert_csv_to_pdf.py $f ${pdfoutput}.pdf "$cat"
done

# Cleanup
echo "Cleaning up directory"
tar -cf backupCSVfiles.tar *.csv 
rm -f *.csv


#!/bin/bash
# Create the race databases

for f in U8 U10 U12 Youth Women Senior Vet50
do
	create_db.py $f
done

#!/usr/bin/bash

# You need to change into the directory with ALL the results files & tell this script which week/round you are loading.
# It will then run ALL the script to update all the races...

# Set PATH to include binary
PATH=$PATH:../bin

# Check we have a week/round!
if [ $# -lt 1 ]; then
    echo "Usage: $0 <num> # Where num is the round number - between 1 and 12"
    exit 1
fi

Week=$1

mkdir league-workingfiles

echo "Running Senior race update"
run-Senior-race-update.sh $Week
echo "Running U10 race update"
run-U10-race-update.sh $Week
echo "Running U12 race update"
run-U12-race-update.sh $Week
echo "Running U8 race update"
run-U8-race-update.sh $Week
echo "Running Vet50 race update"
run-Vet50-race-update.sh $Week
echo "Running Womens race update"
run-Women-race-update.sh $Week
echo "Running Youth race update"
run-Youth-race-update.sh $Week

echo "Running Team awards update"
run-team-awards-results.sh $Week

exit 0

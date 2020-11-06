#!/bin/bash
# For the list of Batch directories in a batch list, outputs the total size of all the batches 

lstat=$(cat ../StatBatches/$1/batches.txt | xargs find | grep -v "_result.csv$" | grep ".csv" | xargs wc -l)
tot=$(printf "$lstat\n" | tail -1 | grep -o "[0-9]*")
sub=$(printf "$lstat\n" | wc -l)
sub=$[$sub-1]
printf "$[$tot-$sub]\n"

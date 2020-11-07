#!/bin/bash
# For a given statbatch, prints all the _result.csv files that belong to the statbatch

cat ../SDSSxGaia/StatBatches/$1/batches.txt | awk '{print "../SDSSxGaia/Batches/"$0}' | xargs -I % find % -type f -name "*result.csv"

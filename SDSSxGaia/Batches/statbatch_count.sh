#!/bin/bash
# For the list of Batch directories in a batch list, output the sizes of the batches

cat ../StatBatches/$1/batches.txt | xargs find | grep -v "_result.csv$" | grep ".csv" | xargs wc -l

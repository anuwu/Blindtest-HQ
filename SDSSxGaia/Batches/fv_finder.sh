#!/bin/bash
# Finds if any result .csv file is in the 5 band format

cat ../StatBatches/Ascom/batches.txt | xargs -I % find % -type f -name "*result.csv" | xargs grep -l z-type

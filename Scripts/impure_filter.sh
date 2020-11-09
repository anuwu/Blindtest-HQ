#!/bin/bash
# Takes as input the impure_pids_temp.csv file and removes lines with no detected peaks
# i.e. 3 commas consecutively

cat $1 | grep -v "[0-9]*,,,\|None"

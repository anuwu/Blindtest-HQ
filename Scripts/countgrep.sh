#!/bin/bash
# For a file, prints its name and the number of occurence of a given regular expression

printf "$2\n"
grep -io $1 $2 | wc -l
#!/bin/bash
# Returns the number of lines in the file which is passed as the argument

wc -l $1 | grep -o "[0-9]* " | tr -d "[:blank:]"

#!/bin/bash
# Add drop.sh, drop.sh, length.sh to /usr/local/bin and remove the .sh extension for this script to work

for var in "$@"
do
        if [ "$var" = "$1" ]
        then
                printf "$(cat $var | head -1)\n"
        fi

        printf "$(drop $var 1)\n"
done

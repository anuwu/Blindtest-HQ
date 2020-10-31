#!/bin/bash

for var in "$@"
do
        if [ "$var" = "$1" ]
        then
                printf "$(cat $var | head -1)\n"
        fi

        printf "$(drop $var 1)\n"
done

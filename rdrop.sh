#!/bin/bash

if [ -e $1 ]
then
        tot=$(wc -l $1 | grep -o "[0-9]* " | tr -d "[:blank:]")
        sub=$2

        if [ $sub -lt 0 ]
        then
                printf "Invalid drop value\n"
                exit
        fi

        if [ $sub -le $tot ]
        then
                cat $1 | head -"$[$tot-$sub]"
        fi
else
        printf "$0 : $1 does not exist\n"
fi

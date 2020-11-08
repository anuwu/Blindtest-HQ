#!/bin/bash
# Helps in viewing a list of cutouts and deciding whether to
# keep or delete them. Enter for keep, 'd' for delete

path="$1/*"

if [ ! -d Keep/ ] 
then
        mkdir Keep/
fi

if [ ! -d Del/ ] 
then
        mkdir Del/
fi

for f in $path 
do
        eog $f & pic_pid=$!
        read -p "d/Enter : " inp
        kill $pic_pid
        if [ "$inp" = "d" ]
        then
                mv $f Del/
        else
                mv $f Keep/
        fi
done 

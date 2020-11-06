#!/bin/bash
# Helps in viewing a list of cutouts and deciding whether to
# keep or delete them. Enter for keep, 'd' for delete

path="$1/*"
for f in $path 
do
        # printf "$f\n"
        eog $f & pic_pid=$!
        read -p "d/Enter : " inp
        kill $pic_pid
        if [ "$inp" = "d" ]
        then
                rm $f
        fi
        # echo $inp
done 

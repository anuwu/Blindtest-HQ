#!/bin/bash
# Makes batches from a list of split csv files into corresponding batch folders 

inpref=$1
outpref=$2
stnum=$3
endnum=$4

i=$stnum
while [ $i -le $endnum ]
do
        incsv="$inpref$i.csv"
        fold="$outpref$i"
        outcsv="$fold/$outpref$i.csv"
        mkdir $fold
        mv $incsv $outcsv
        # printf "$incsv $fold $outcsv\n"
        i="$[$i+1]"
done

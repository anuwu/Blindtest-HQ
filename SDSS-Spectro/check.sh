#!/bin/bash

i="1"
res="Batches/Spectro$i/Spectro$[i]_result.csv"
while [[ -f "$res" ]] 
do
	printf "$i - $(wc -l $res)\n"
	i="$[$i+1]"
	res="Batches/Spectro$i/Spectro$[i]_result.csv"
done

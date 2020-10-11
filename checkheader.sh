fname=$1
dir=$(pwd)
i="1"
csvfile1=$dir/$fname/$fname$i/$fname${i}.csv
csvfile2=$dir/$fname/$fname$i/$fname${i}_result.csv
while [[ -f "$csvfile1" ]] && [[ -f "$csvfile2" ]] 
do
	col1=$(head -1 $csvfile1)
	col1="${col1:0:5}"
	col2=$(head -1 $csvfile2)
	col2="${col2:0:5}"

	printf "$col1 | $col2\n"
	i="$[$i+1]"
	csvfile2=$dir/$fname/$fname$i/$fname${i}_result.csv
	csvfile1=$dir/$fname/$fname$i/$fname${i}.csv	
done

i="$[$i-1]"
printf "Cumulatively completed $1 upto = $i\n"

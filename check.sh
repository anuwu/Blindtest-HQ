fname=$1
dir=$(pwd)
i="1"
while test -f "$dir/$fname/$fname$i/$fname${i}_result.csv"
do
	i="$[$i+1]"
done

i="$[$i-1]"
printf "Cumulatively completed $1 upto = $i\n"

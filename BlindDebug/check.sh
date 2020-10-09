fname="BlindDebug"
i="1"
while test -f "$fname$i/$fname${i}_result.csv"
do
	i="$[$i+1]"
done

i="$[$i-1]"
printf "Cumulatively completed upto = $i\n"

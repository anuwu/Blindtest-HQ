fn=$1
i=$2
j=$3
while [ $i -le $j ]
do
	ol="$fn$i/$fn${i}_Complete_result.csv"
	nu="$fn$i/$fn${i}_result.csv"
	[ -f $ol ] && mv $ol $nu
	i="$[$i+1]" 
done

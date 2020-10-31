files=$(ls Cutouts/[0-9]*[0-9]-p?.jpeg)
# echo $files

for f in $files
do 
        # printf "$f\n"
        r=$(printf "$f" | tr - _)
        # printf "$r\n"
        mv $f $r
done

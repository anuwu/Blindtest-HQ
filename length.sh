wc -l $1 | grep -o "[0-9]* " | tr -d "[:blank:]"

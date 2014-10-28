#!/bin/bash

for filename in $@ 
do 
	fName=$(basename "$filename")
	extension="${filename##*.}"
	fName="${filename%.*}"
	echo "select 'Processing .... $filename';"  >> /home/saguinag/CategoryPaths/ssspLoadTables.sql
	echo "load data local infile '$filename' into TABLE $fName;" >> /home/saguinag/CategoryPaths/ssspLoadTables.sql
done

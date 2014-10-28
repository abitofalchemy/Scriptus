#!/bin/bash

for filename in $@ 
do 
	echo $filename
	fName=$(basename "$filename")
	extension="${filename##*.}"
	fName="${filename%.*}"
	echo ": $fName"
	echo "CREATE TABLE $fName (id INT PRIMARY KEY, dist INT);" >> /home/saguinag/CategoryPaths/ssspCreateTables.sql
done

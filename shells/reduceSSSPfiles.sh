#!/bin/bash

#echo $1/*txt
for i in $1/*txt ; 
do 	
	echo $i;
	outfile='/data/zliu8/filtered_sssp/';
	outfile=$outfile$i'.flt'
	if [ ! -f $outfile ]; then
		echo $outfile
		grep -e '^[0-9]\+\s[0-9]\{1,3\}' $i > $outfile
	fi
done

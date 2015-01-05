#!/bin/bash

for file in *; 
do 
	ls $file |	perl -ne '/sssp_([0-9]+).txt/; print "$1\n"' ; 
done
#echo `expr match "sssp_9287211.txt" '([a-z]+).txt'`   # abcABC1

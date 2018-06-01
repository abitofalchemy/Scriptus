#!/bin/bash

#echo $1/*txt
for i in $1*dot ; 
do 	
	echo $i;
	grep -e 'a1=' $i | wc -l 
done

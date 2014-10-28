#!/bin/bash

#echo $1/*txt
for i in $1/*txt ; 
do 	sort -o $i ($i | sed -r 's/^.{17}//') ; done

#!/bin/bash

# example 1
#convert myfile.jpg myfile.eps

# example 2
#for file in file1.jpg file2.jpg file3.jpg; do
#		    echo convert "$file" $(echo "$file" | sed 's/\.jpg$/\.eps/')
#			done

for f in *.png
do
	g=`echo "$f" | sed 's/\.png$/\.eps/'`
	echo "$f -> $g" 1>&2
	#jpegtopnm $f | pnmtopng > $g
	convert $f eps3:$g
	done

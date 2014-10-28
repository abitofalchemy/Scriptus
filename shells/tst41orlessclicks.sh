#!/bin/sh 

## check if the dat files have paths 
for f in *.dat; do grep ',0$' $f;  done


#!/bin/bash

# create an array with all the filer/dir inside ~/myDir
arr=(~/myDir/*)

# iterate through array using a counter
for ((i=0; i<${#arr[@]}; i++)); do
      #do something to each element of array
          echo "${arr[$i]}"
        done

#!/bin/bash

#find /data/zliu8/sssp/sssp_18916317.txt -type f -exec sed -i.bak "s/3.40282e+38/-1/g" {} \;
find . -type f -name "*.txt" -exec sed -i.bak "s/3.40282e+38/-1/g" {} \;

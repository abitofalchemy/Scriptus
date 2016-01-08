#!/bin/bash

## working with parallel

ls ~/Research/CategoryPaths/wiki_data/adjlist/

## Testing parallel by feeding using 1 pair 
head -n1 ~/Research/CategoryPaths/wiki_data/wpg_paths/wikipedia_games_set.tsv | parallel --colsep '\t' ./mycc {1} {2}  


find . -iname '*.tsv' -type f -print | parallel echo {}

## for all file of type .dat cut two columns
find . -iname '*.dat' -type f -print | parallel cut -d "," -f 1,3 {} > game_endpts{}

# another way 
parallel "cut -d ',' -f 1,3 {} >{.}_gep" ::: ../ssspGamesDatFiles/*.dat

## change the ',' delimeter to a tab '\t'
#find . -iname '*_gep' -type f -print | sed 's/<TAB>/,/g'
find . -iname '*_gep' -type f -print | parallel 'sed "s/,/''\t''/g" {} >{.}.tsv'

## remove the header from file (first line)
find . -iname '*.tsv' -type f -print | parallel 'sed "1d" {} >{.}tmpfile; mv {.}tmpfile {}'

## For each line of a file do:
find . -iname '*.tsv' -type f -print | parallel -a {} head -n1

head -n1 ~/Research/CategoryPaths/wiki_data/wpg_paths/wikipedia_games_set.tsv | parallel --colsep '\t' ./mycc {1} {2}  

## sort a file by column 2
ls -1 /tmp/pg_rnk_bspl.* | parallel sort -n -r -k2 -o {}_sorted {}




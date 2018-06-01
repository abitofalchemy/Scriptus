`find . -name '*.pl' -type f -exec grep "^e(" {} + | awk '{ print $3 }' | grep "^[^\(]" >/tmp/example_relations_from_pl.tsv`



find . -print0 | while read -d $'\0' file; do echo -v "$file" ; done

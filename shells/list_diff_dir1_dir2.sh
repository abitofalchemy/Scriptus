find StripAnalyzer/*m -print0 | while read -d $'\0' file; 
do 
	diff -iqbwBE "$file" ~/WindForce/iOS/Serim_iOS/"$file" ; 
done

StripAnalyzer/*m -print0 | while read -d $'\0' file; do diff -iqbwBE "$file" ~/WindForce/iOS/Serim_iOS/"$file";done



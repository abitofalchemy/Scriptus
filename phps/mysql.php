<?php
// http://stackoverflow.com/questions/25190050/compare-2-csv-file-with-1-column-each-in-php
// Tell PHP that we're using UTF-8 strings until the end of the script
mb_internal_encoding('UTF-8');
 
// Tell PHP that we'll be outputting UTF-8 to the browser
mb_http_output('UTF-8');
 
// Our UTF-8 test string
$string = 'Êl síla erin lû e-govaned vîn.';
 
// Transform the string in some way with a multibyte function
// Note how we cut the string at a non-Ascii character for demonstration purposes
$string = mb_substr($string, 0, 15);
 
// Connect to a database to store the transformed string
// See the PDO example in this document for more information
// Note the `charset=utf8mb4` in the Data Source Name (DSN)
$link = new PDO(
    'mysql:host=localhost;dbname=wikipedia;charset=utf8mb4',
    'saguinag',
    'dsg1!0xB',
    array(
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_PERSISTENT => false
    )
);
		/*foreach ($link->query('select page_title from page limit 1000;') as $row){
			echo $row['page_title']; 
		}*/
		$file = file('file.csv');
		$list = implode('',$file);
		echo $list;
		$stmt = $link->query('select page_id,page_title from page where page_title IN ($list);');
		$results = $stmt->fetchAll(PDO::FETCH_ASSOC);
		echo $results;
?>

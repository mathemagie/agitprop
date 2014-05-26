<?php
error_reporting(E_ALL ^ E_NOTICE);
ini_set('display_errors', 1);

$hostname = "localhost";
$dbname = "pegman";
$username = "root";
$pw = "root";
$pw = "@PASS@";
$debug = $_GET['debug'];

if (!$link_mysql = mysql_connect($hostname, $username, $pw)) {
    echo 'Could not connect to mysql';
    exit;
}

if (!mysql_select_db($dbname, $link_mysql)) {
    echo 'Could not select database';
    exit;
}



if ($debug) {
    $sql    = "SELECT * FROM urls";
    $result = mysql_query($sql, $link_mysql);
    $results = array();
    while($row = mysql_fetch_array($result)) {
     $results[] = array(
          'url' => $row['url'],
        );
    }
    $json = json_encode($results);
    echo $json;
}


function addUrl($url,$link) {
    $sql_select = "select * from urls where url='" . $url . "'";
    $result = mysql_query($sql_select, $link);
    $rows = mysql_num_rows($result);
    if ($rows == '0') {
        $sql = "INSERT into urls values ('" . $url . "')";
         mysql_query($sql,$link);
        return 1;
    }else {
        return 0;
    }
}

require_once('simple_html_dom.php');
$url  = 'http://www.google.com/search?hl=en&safe=active&tbo=d&site=&source=hp&q=pegman&tbs=qdr:h';
if ($debug) echo "<br/><br/>" . $url;
$html = file_get_html($url);

$linkObjs = $html->find('h3.r a');
$i = 0;
foreach ($linkObjs as $linkObj) {
    $title = trim($linkObj->plaintext);
    $link  = trim($linkObj->href);
    
    // if it is not a direct link but url reference found inside it, then extract
    if (!preg_match('/^https?/', $link) && preg_match('/q=(.+)&amp;sa=/U', $link, $matches) && preg_match('/^https?/', $matches[1])) {
        $link = $matches[1];
    } else if (!preg_match('/^https?/', $link)) { // skip if it is not a valid link
        continue;    
    }
    
    if ($debug) {
        echo '<p>Title: ' . $title . '<br />';
        echo 'Link: ' . $link . '</p>';
    }
    $res = addUrl($link,$link_mysql);
    if ($res) $i = $i + 1;
   
}
echo $i;
?>

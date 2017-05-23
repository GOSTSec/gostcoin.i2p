<?php
require_once("config.php");
include("class/language.php");
include("class/pages.php");

$pages = new pages(); 
$pages->GetPage("header");
//echo $pages->_("nameproject");
if(!isset($_GET['page']))
 $pages->GetPage("main");
else
 $pages->GetPage($_GET['page']);

?>


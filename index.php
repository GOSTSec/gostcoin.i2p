<?php
require_once("config.php");
include("class/pages.php");
if(isset($_GET['lang']))
 $pages = new pages($_GET['lang']);
else
  $pages = new pages();
$pages->GetPage("header");

if(!isset($_GET['page']))
 $pages->GetPage("main");
else
 $pages->GetPage($_GET['page']);

?>


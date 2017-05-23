<?php
require_once("config.php");
include("class/language.php");
include("class/pages.php");
if(isset($_GET['lang']))
 $pages = new pages($_GET['lang']);
else
  $pages = new pages( locale_accept_from_http($_SERVER['HTTP_ACCEPT_LANGUAGE']) );
$pages->GetPage("header");

if(!isset($_GET['page']))
 $pages->GetPage("main");
else
 $pages->GetPage($_GET['page']);

?>


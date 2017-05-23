<?php
class pages extends language
{
	public function __construct($lang='en_US')
	{
		if(!file_exists(LANG.$lang."."."php")) return $this->lang="en_US";
		$this->lang=$lang;
	}
	public function ParseTemplate($what)
	{
		$what = str_replace(LANG_ARRAY, $this->LanguageConstant($this->lang), $what );
		return $what;
	}
	
	public function GetPage($namepage)
	{
		if(! file_exists(PAGES."/".$namepage.".tlp") ) return header("Location: .");		 
		 $page = fopen(PAGES."/".$namepage.".tlp","rb");
		 $content = "";
		 
		 while ( !feof($page) ) 
		   $content .= fread($page, PARTOFFILE);
		 $content = $this->ParseTemplate($content);
		 return print (	$content );

	}
	public function __destruct() {
			 clearstatcache();
	}

}
?>

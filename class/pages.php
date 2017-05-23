<?php
class pages extends language
{
	public function ReadSomeFile($file)
	{
	 $content = "";
	 while ( !feof($file) ) 
		$content .= fread($file, PARTOFFILE);
	 fclose($file);
	 return $content;
	}
	public function create_cache($namepage,$content)
	{
		 $page = fopen(CACHE."/".$this->lang."_".$namepage.".htm","wb");
		 if(!fwrite($page,$content)) return die("Permission denied");
		 fclose($page);
	}
	public function __construct()
	{
		$this->lang=$this->getLang();
	}
	public function ParseTemplate($what)
	{
		$what = str_replace(LANG_ARRAY, $this->LanguageConstant($this->lang), $what );
		return $what;
	}
	
	public function GetPage($namepage)
	{
		if(file_exists(CACHE."/".$this->lang."_".$namepage.".htm"))
		{
			$namefile = CACHE."/".$this->lang."_".$namepage.".htm";
			$page = fopen($namefile,"rb");
			if(LIFECACHE != 0)
			 if(filemtime($namefile) >= (filemtime($namefile)+LIFECACHE) )
			 {
				 if(!unlink($namefile))
					die( "Permission denied" );
			 }
			return print $this->ReadSomeFile($page);
		}// IF CACHE
		
		if(! file_exists(PAGES."/".$namepage.".tlp") ) return header("Location: .");		 
		 $page = fopen(PAGES."/".$namepage.".tlp","rb");
		 ///////////
		 $content = $this->ReadSomeFile($page);
		 $content = $this->ParseTemplate($content);
		 /////////
		 $this->create_cache($namepage,$content);
		 return print (	$content );

	}
	public function __destruct() {
			 clearstatcache();
	}

}
?>

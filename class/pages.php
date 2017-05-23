<?php
class pages extends language
{
	public function create_cache($namepage,$content)
	{
		 $page = fopen(CACHE."/".$this->lang."_".$namepage.".php","wb");
		 if(!fwrite($page,$content)) return die("Permission denied");
		 fclose($page);
	}
	public function __construct()
	{
		$this->lang=$this->getLang();
	}
	public function ParseTemplate($what)
	{
		$what = str_replace($this->LanguageConstantGet("default"), $this->LanguageConstantGet($this->lang), $what );
		return $what;
	}
	
	public function GetPage($namepage)
	{
		if(file_exists(CACHE."/".$this->lang."_".$namepage.".php"))
		{
			$namefile = CACHE."/".$this->lang."_".$namepage.".php";
			include($namefile);
			if(LIFECACHE != 0)
			 if(filemtime($namefile) >= (filemtime($namefile)+LIFECACHE) )
			 {
				 if(!unlink($namefile))
					die( "Permission denied" );
			 }
			 return 1;
		}// IF CACHE
		
		if(! file_exists(PAGES."/".$namepage.".tlp") ) return header("Location: .");		 
		 $page = fopen(PAGES."/".$namepage.".tlp","rb");
		 ///////////
		 $content = $this->ReadSomeFile($page);
		 $content = $this->ParseTemplate($content);
		 /////////
		 $this->create_cache($namepage,$content);
		 $this->GetPage($namepage);

	}
	public function __destruct() {
			 clearstatcache();
	}

}
?>

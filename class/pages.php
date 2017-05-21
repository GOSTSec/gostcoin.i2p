<?php
class pages
{
	private $lang;
	public function __construct($lang='en')
	{
		$this->lang=$lang;
	}
	public function findPage($namepage)
	{
		if(! (file_exists(PAGES.$this->lang."/".$namepage.".php"))  ) 
		{
		 if(! file_exists(PAGES.$this->lang."/".$namepage.".htm") ) return header("Location: .");
		 $page = fopen(PAGES.$this->lang."/".$namepage.".htm","rb");
		 $content = '';
		 
		 while ( !feof($page) ) 
		   $content .= fread($page, PARTOFFILE);
		 
		 return print (	$content );
		}else { 
		include(PAGES.$this->lang."/".$namepage.".php");
		return 1;
	    }
	}
	public function GetPage($namepage)
	{
		if(! $page = $this->findPage($namepage) ) return 0;
		return $page;
	}
	public function __destruct() {
			 clearstatcache();
	}

}
?>

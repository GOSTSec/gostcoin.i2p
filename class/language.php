<?php
class language
{
	protected $lang;
	
	protected function ReadSomeFile($file)
	{
	 if($file == NULL) return 0;
	 $content = "";
	 while ( !feof($file) ) 
		$content .= fread($file, PARTOFFILE);
	 fclose($file);
	 return $content;
	}
	public function checkExistLang($filename)
	{
			if(file_exists(LANG.$filename.".ini")) return 1;
			if(file_exists(LANG.$filename.".json")) return 1;
			return 0;
	}
	protected function getLang()
	{

		if(
		isset($_COOKIE['lang']) && 
		is_string($_COOKIE['lang']) && 
		file_exists(LANG.$_COOKIE['lang'].".ini") 
		) return $_COOKIE['lang'];
		
		elseif( $this->checkExistLang( locale_accept_from_http($_SERVER['HTTP_ACCEPT_LANGUAGE']) ) )
			return locale_accept_from_http($_SERVER['HTTP_ACCEPT_LANGUAGE']);
		else
		 return DEFAULT_LANG;
		
	}
	protected function GetLangFile($filename)
	{
			if(file_exists(LANG.$filename.".ini"))
			 return parse_ini_file(LANG.$filename.".ini"); 
			   
			elseif(file_exists(LANG.$filename.".json"))
			 return json_decode($this->ReadSomeFile(LANG.$filename.".json"),1);
			
			else
			 return die("Not can find a language file".$filename."<br>");

	}
	protected function LanguageConstantGet($lang=NULL)
	{
		if($lang == NULL)
		 return $this->GetLangFile("default");
		return $this->GetLangFile($lang);
////////////////////////////////////////////////////////////////////////
	}
}
?>

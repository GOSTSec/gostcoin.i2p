<?php
class language
{
	protected $lang;
	public function getLang()
	{

		if(
		isset($_COOKIE['lang']) && 
		is_string($_COOKIE['lang']) && 
		file_exists(LANG.$_COOKIE['lang']."."."php") 
		) return $_COOKIE['lang'];
		
		elseif( file_exists(LANG.locale_accept_from_http($_SERVER['HTTP_ACCEPT_LANGUAGE']).".php") )
			return locale_accept_from_http($_SERVER['HTTP_ACCEPT_LANGUAGE']);
		else
			return DEFAULT_LANG;

	}
	public function LanguageConstant($lang=NULL)
	{
		if($lang == NULL || $lang == "en_US")
		{
			require_once("lang/".DEFAULT_LANG.".php");
			return SOME_LANG;	
		}
////////////////////////////////////////////////////////////////////////
			require_once(LANG.$lang.".php");
			return SOME_LANG;
	}
}
?>

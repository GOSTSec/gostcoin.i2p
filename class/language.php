<?php
class language
{
	protected $lang;
	public function LanguageConstant($lang=NULL)
	{
		if($lang == NULL || $lang == "en_US")
		{
			require_once("lang/en_US.php");
			return SOME_LANG;	
		}
////////////////////////////////////////////////////////////////////////
			require_once(LANG.$lang.".php");
			return SOME_LANG;
	}
}
?>

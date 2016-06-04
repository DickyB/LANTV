<?php

$MASTERFILE="master.list";
$TEMPFILE="master.temp";
$MYSQL_HOST='127.0.0.1';
$MYSQL_PORT='3306';
$MYSQL_DATABASE='databasename';
$MYSQL_USER='username';
$MYSQL_PASS='password';
$MYSQL_TABLE='tablename';



function addifnot($vfull,$vfile,$vlen)
{

$connect = mysql_connect($GLOBALS['MYSQL_HOST'],$GLOBALS['MYSQL_USER'],$GLOBALS['MYSQL_PASS']);
if (!$connect)
	{
	die("MySQL could not connect.");
	}
$vfull=trim($vfull);
$vfile=trim($vfile);
$vfull=mysql_real_escape_string($vfull);
$vfile=mysql_real_escape_string($vfile);
$DB = mysql_select_db($GLOBALS['MYSQL_DATABASE']);
if(!$DB){die("MySQL could not select Database.");}
$Query = mysql_query("SELECT * FROM " . $GLOBALS['MYSQL_TABLE'] . " WHERE fullpath='$vfull'");
if(!$Query)
	{
	echo $vfull,"\n";
	}

if($Query)
	{
	$NumRows=mysql_num_rows($Query);
	if($NumRows==0)
		{
		if(!mysql_query("INSERT INTO " . $GLOBALS['MYSQL_TABLE'] . " (fullpath, filename, length) VALUES('$vfull', '$vfile', '$vlen')"))
			{
			die("We dinna do it, Cap'n");
			}
		}
	}
}




$mfl='master.list';
$fp = fopen($mfl,'rb'); if($fp) $GLOBALS['lines'] = explode("\n",fread($fp,filesize($mfl)));
$idx=0;
while ($idx < (count($GLOBALS['lines'])-2))
  {
  $fpath=trim($GLOBALS['lines'][$idx],"\n");
  $fname=trim($GLOBALS['lines'][$idx+1],"\n");
  $flen=trim($GLOBALS['lines'][$idx+2],"\n");
  $flen=substr($flen,0,8);
  if($fpath != "")
    {
    addifnot($fpath,$fname,$flen);
    }
  $idx=$idx+3;
  } 
//prune out missing video records
$connect = mysql_connect($GLOBALS['MYSQL_HOST'],$GLOBALS['MYSQL_USER'],$GLOBALS['MYSQL_PASS']);
if (!$connect)
	{
	die("MySQL could not connect.");
	}
$DB = mysql_select_db($GLOBALS['MYSQL_DATABASE']);
if(!$DB){die("MySQL could not select Database.");}
$Query = mysql_query("SELECT * FROM " . $MYSQL_TABLE);
$axelist[]=array();
while ($row = mysql_fetch_array($Query))
  {
  if(!file_exists($row['fullpath']) )
    {
    $axelist[]=$row['fullpath'];  
    }
  }

$cnt=1;
while($cnt<count($axelist))
  {
  print "DELETE FROM " . $MYSQL_TABLE . " WHERE fullpath='" . $axelist[$cnt] . "'";
  print "\n";
  $Query = mysql_query ("DELETE FROM " . $MYSQL_TABLE . " WHERE fullpath=\"" . $axelist[$cnt] . "\"");
  if(!$Query)
    {
    die("Shinola.");
    }
  print $axelist[$cnt];
  print "\n";
  $cnt++;
  }

?>

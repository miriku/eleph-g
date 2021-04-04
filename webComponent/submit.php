<?php
	# for dev
	$DEBUG = 0;

	# load input
	extract($_POST);

	# give it a quick one over for content
	$GameName = filter_var($GameName, FILTER_SANITIZE_STRING);
	if(!is_numeric($Submitter)) die("bad input, error code 0");
	if(!is_numeric($GameLength)) die("bad input, error code 1");
	if(!is_numeric($Players)) die("bad input, error code 2");
	if(!is_numeric($WaitTime)) die("bad input, error code 3");

	# now update the state 'database' file. to do this we will read it to find
	# out what the next id should be, then write the new line.
		
	# first open output 'database' in read write mode
	$f=fopen("list.txt", "r+");

	# keep track of highest ID so far
	$maxid=-1;
		
	# grab lock. this will freeze execution until lock is grabbed. the failure case is 
	# operating system rejecting the request and not a locked a file.
	if(flock($f,LOCK_EX))
	{
		# grab a line
		while($l=fgets($f))
		{	
			# tab split
			$vars = explode("\t", $l);

			# grab id, but only if it's larger than current. they should be exclusively 
			# incrementing as you go, but a bit of safety checking never hurt 
			# anyone
			if($vars[0] > $maxid) $maxid = $vars[0];
		}

		# done reading so that was largest id. let's make unique id
		$maxid++;

		# generate output string
		$output = $maxid."\t".$GameName."\t".$Players."\t".$WaitTime."\t".$Submitter."\n";
	
		# dev helper
		if($DEBUG)
		{
			print "<pre>";
			print "maxid = $maxid\n";
			print "GameName = $GameName\n";
			print "Players = $Players\n";
			print "WaitTime = $WaitTime\n";
			print "Submitter = $Submitter\n";
			print "output = $output\n";
		}

		# file pointer is now at end and we can write a new line
		fwrite($f, $output);
		
		# unlock file
		flock($f,LOCK_UN);
		# php should add a funlock() function that does the above
	}
	else
	{
		# if we're here then something went wrong. specifically
		# flock could not lock the file. your OS is not compatible 
		# with this bot. you'll need an actual database of some sort
		die("disk error, code 1");
	}

	print "Game created. <br><br>\n";
	print "Please allow the bot up to a minute to update and display your game in discord. <br><br>\n";
	print "You may safely close this browser tab. <br><br>\n";
?>

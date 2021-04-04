<?php
	$num = $_GET['i'];
	if(!is_numeric($num)) die;
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
</head>

<body>
<form action="submit.php" method="POST">

	<input type=hidden name=Submitter value=<?php echo $num; ?>>

	Game Name
	<input name="GameName" type="text">
	<br><br>

	Game Length (estimated)
  <select name="GameLength">
	  <option value="1">Less than an hour</option>
	  <option value="2">1-2 hours</option>
	  <option value="3">2-3 hours</option>
	  <option value="4">3-4 hoursr</option>
	  <option value="5">4+ hours</option>
	</select>
	<br><br>

	How many more players do you need to start
  <input type="radio" value="1" name="Players">1</label>
  <input type="radio" value="2" name="Players">2</label>
	<input type="radio" value="3" name="Players">3</label>
	<input type="radio" value="4" name="Players">4</label>
	<input type="radio" value="5" name="Players">5</label>
	<br><br>

	How long are you willing to wait to start
	<select name="WaitTime">
	  <option value="1">1 hour</option>
	  <option value="2">2 hours</option>
	  <option value="3">3 hours</option>
	  <option value="4">4 hours</option>
	  <option value="5">5 hours</option>
	  <option value="6">As long as it takes, leave it open</option>
	</select>
	<br><br>

	<input type=submit value=submit name=submit>
		
</form>
</body>
</html>

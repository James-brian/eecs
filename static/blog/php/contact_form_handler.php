<?php

if(isset($_POST['submit'])) {
	$name = $_POST['name'];
	$country = $_POST['country'];
	$mailFrom = $_POST['mail'];
	$message = $_POST['message'];
	$subject = $_POST['subject'];

	$mailTo ="brianoigo785@gmail.com";
	$headers = "From: ".$mailFrom;
	$txt = "You have received an e-mail from ".$name.".\n\n".$message;

	mail($mailTo,$subject,$txt,$headers);
	header("Location: contact.html");
   }

?>
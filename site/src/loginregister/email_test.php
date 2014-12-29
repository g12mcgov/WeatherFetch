<?php

## PATH MUST CHANGE 
require_once '/Users/grantmcgovern/vendor/swiftmailer/swiftmailer/lib/swift_required.php';
 
//Create the Transport
$transport = Swift_SmtpTransport::newInstance('smtp.gmail.com', 465, 'ssl')
  ->setUsername('grantmcgovern.mcgovern@gmail.com')
  ->setPassword('#')
  ;
 
/*
You could alternatively use a different transport such as Sendmail or Mail:
 
//Sendmail
$transport = Swift_SendmailTransport::newInstance('/usr/sbin/sendmail -bs');
 
//Mail
$transport = Swift_MailTransport::newInstance();
*/
 
//Create the Mailer using your created Transport
$mailer = Swift_Mailer::newInstance($transport);
 
//Create a message
$message = Swift_Message::newInstance('Wonderful Subject')
  ->setFrom(array('grantmcgovern.mcgovern@gmail.com' => 'WeatherFetch'))
  ->setTo(array('mcgoga12@wfu.edu' => 'A name'))
  ->setBody('Here is the message itself')
  ;
   
//Send the message
$result = $mailer->send($message);
 
/*
You can alternatively use batchSend() to send the message
 
$result = $mailer->batchSend($message);
*/
 
?>

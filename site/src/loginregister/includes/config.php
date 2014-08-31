<?php
require_once 'vendor/swiftmailer/swiftmailer/lib/swift_required.php';

ob_start();
session_start();

//set timezone to UTC Time
date_default_timezone_set('UTC');

//database credentials
define('DBHOST','localhost');
define('DBUSER','root');
define('DBPASS','nantucket');
define('DBNAME','WeatherFetchDB');

$transport = Swift_SmtpTransport::newInstance('smtp.gmail.com', 465, 'ssl')
  ->setUsername('no-reply@weatherfetch.com')
  ->setPassword('grantmcgovern1')
  ;

$mailer = Swift_Mailer::newInstance($transport);

//application address

// Will need to be updated to 'www.weatherfetch.com' when live on EC2 instance
define('DIR','www.weatherfetch.com');
define('SITEEMAIL','no-reply@weatherfetch.com');

try {

	//create PDO connection 
	$db = new PDO("mysql:host=".DBHOST.";port=8889;dbname=".DBNAME, DBUSER, DBPASS);
	$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

} catch(PDOException $e) {
	//show error
    echo '<p class="bg-danger">'.$e->getMessage().'</p>';
    exit;
}

//include the user class, pass in the database connection
include('classes/user.php');
$user = new User($db); 
?>

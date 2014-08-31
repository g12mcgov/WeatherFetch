<?php require('includes/config.php'); 

//if logged in redirect to members page
if( $user->is_logged_in() ){ header('Location: memberpage.php'); } 

//if form has been submitted process it
if(isset($_POST['submit'])){

	//email validation
	if(!filter_var($_POST['EmailAddress'], FILTER_VALIDATE_EMAIL)){
	    $error[] = 'Please enter a valid email address';
	} else {
		$stmt = $db->prepare('SELECT EmailAddress FROM members WHERE EmailAddress = :EmailAddress');
		$stmt->execute(array(':EmailAddress' => $_POST['EmailAddress']));
		$row = $stmt->fetch(PDO::FETCH_ASSOC);

		if(empty($row['EmailAddress'])){
			$error[] = 'Email provided is not on recognised.';
		}
			
	}

	//if no errors have been created carry on
	if(!isset($error)){

		//create the activasion code
		$token = md5(uniqid(rand(),true));

		try {

			$stmt = $db->prepare("UPDATE members SET resetToken = :token, resetComplete='No' WHERE EmailAddress = :EmailAddress");
			$stmt->execute(array(
				':EmailAddress' => $row['EmailAddress'],
				':token' => $token
			));

			$message = Swift_Message::newInstance('Password Reset')
  			->setFrom(array('grantmcgovern.mcgovern@gmail.com' => 'WeatherFetch'))
  			->setTo($row['EmailAddress'])
 				->setBody("Someone requested that the password be reset. \n\nIf this was a mistake, just ignore this email and nothing will happen.\n\nTo reset your password, visit the following address: ".DIR."resetPassword.php?key=$token")
  			;
   
			//Send the message
			$result = $mailer->send($message);


			//redirect to index page
			header('Location: login.php?action=reset');
			exit;

		//else catch the exception and show the error.
		} catch(PDOException $e) {
		    $error[] = $e->getMessage();
		}

	}

}

//define page title
$title = 'Reset Account';

//include header template
require('layout/header.php'); 
?>

<body class="reset">
	<div class="resetForm">
		<div class="container">
			<div class="row">
			    <div class="col-xs-12 col-sm-8 col-md-6 col-sm-offset-2 col-md-offset-3">
					<form role="form" method="post" action="" autocomplete="off">
						<div class="centered">
							<h1>Reset Password</h1>
						</div>
						<hr>
						<?php
						//check for any errors
						if(isset($error)){
							foreach($error as $error){
								echo '<p class="bg-danger">'.$error.'</p>';
							}
						}
						if(isset($_GET['action'])){

							//check the action
							switch ($_GET['action']) {
								case 'active':
									echo "<h2 class='bg-success'>Your account is now active you may now log in.</h2>";
									break;
								case 'reset':
									echo "<h2 class='bg-success'>Please check your inbox for a reset link.</h2>";
									break;
							}
						}
						?>
						<div class="form-group">
							<input type="email" name="EmailAddress" id="EmailAddress" class="form-control input-lg" placeholder="Email" value="" tabindex="1">
						</div>
						<hr>
						<div class="centered">
							<p><a href='login.php'>Back to login page</a></p>
						</div>
						<div class="centered">
							<input type="submit" name="submit" value="Sent Reset Link" class="btn btn-primary btn-block btn-lg" id="resetButton" tabindex="2">
						</div>
					</form>
				</div>
			</div>
		</div>
	</div>
</body>

<?php 
//include header template
require('layout/footer.php'); 
?>
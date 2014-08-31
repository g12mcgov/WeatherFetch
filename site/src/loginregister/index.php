<?php require('includes/config.php'); 

//if logged in redirect to members page
//if( $user->is_logged_in() ){ header('Location: memberpage.php'); } 

//if form has been submitted process it
if(isset($_POST['submit'])){

	//very basic validation
	if(strlen($_POST['username']) < 3){	
		$error[] = 'Username is too short.';
	} else {
		$stmt = $db->prepare('SELECT username FROM members WHERE username = :username');
		$stmt->execute(array(':username' => $_POST['username']));
		$row = $stmt->fetch(PDO::FETCH_ASSOC);

		if(!empty($row['username'])){
			$error[] = 'Username provided is already in use.';
		}
			
	}

	if(strlen($_POST['password']) < 3){
		$error[] = 'Password is too short.';
	}

	if(strlen($_POST['passwordConfirm']) < 3){
		$error[] = 'Confirm password is too short.';
	}

	if($_POST['password'] != $_POST['passwordConfirm']){
		$error[] = 'Passwords do not match.';
	}


	//Zipcode Validation 
	if(strlen($_POST['Zipcode']) < 5){
		$error[] = 'Zipcode is not valid. Please check your input.';
	}


	//email validation
	if(!filter_var($_POST['EmailAddress'], FILTER_VALIDATE_EMAIL)){
	    $error[] = 'Please enter a valid email address';
	} else {
		$stmt = $db->prepare('SELECT EmailAddress FROM members WHERE EmailAddress = :EmailAddress');
		$stmt->execute(array(':EmailAddress' => $_POST['EmailAddress']));
		$row = $stmt->fetch(PDO::FETCH_ASSOC);

		if(!empty($row['EmailAddress'])){
			$error[] = 'Email provided is already in use.';
		}
			
	}


	$current_date = date("Y-m-d");
	$space = ' ';
	$time_input = $_POST['time'];
	
	// Array of 2, 0th index carrying the timezone tag.
	$timezone = $time_input[0];

	$time = date('H:i:s',strtotime($current_date.$space.$time_input[1]));

	//if no errors have been created carry on
	if(!isset($error)){

		//hash the password
		$hashedpassword = $user->password_hash($_POST['password'], PASSWORD_BCRYPT);

		//create the activasion code
		$activasion = md5(uniqid(rand(),true));

		try {

			//insert into database with a prepared statement
			$stmt = $db->prepare('INSERT INTO members (username,password,EmailAddress,Time,Timezone,Zipcode,active) VALUES (:username, :password, :EmailAddress, :Time, :Timezone, :Zipcode, :active)');
			$stmt->execute(array(
				':username' => $_POST['username'],
				':password' => $hashedpassword,
				':EmailAddress' => $_POST['EmailAddress'],
				':Time' => $time,
				':Timezone' => $timezone,
				':Zipcode' => $_POST['Zipcode'],
				':active' => $activasion
			));
			$id = $db->lastInsertId('memberID');

			$message = Swift_Message::newInstance('Activate your WeatherFetch')
  			->setFrom(array('no-reply@weatherfetch.com' => 'WeatherFetch'))
  			->setTo($_POST['EmailAddress'])
 				->setBody("Thank you for registering with WeatherFetch.\n\n\n To activate your account, please click on the following link:\n\n ".DIR."activate.php?x=$id&y=$activasion\n\n Thanks,\n\n WeatherFetch \n\n")
  			;
   
			//Send the message
			$result = $mailer->send($message);

			//redirect to index page
			header('Location: index.php?action=joined');
			exit;

		//else catch the exception and show the error.
		} catch(PDOException $e) {
		    $error[] = $e->getMessage();
		}

	}

}

//define page title
$title = 'WeatherFetch';

//include header template
require('layout/header.php'); 
?>

<a name="toTop"></a>
	<div class="container-fluid">
		<nav class="navbar navbar-static-top" role="navigation">
			<div class="navbar-inner" id="navBarArea">
				<a class="brand" href="index.php"></a>
			  </div>
		  </div>
		</nav>
	</div>
	<div class="centerPanel">
		<div class="container-fluid" id="registrationText">
			<h1><b>Hate your weather app? Join us!</b></h1>
		</div>
		<div class="container-fluid">
			<div class="row">
				<div class="column1">
					<div class="col-md-4"> <!-- Placeholder -->
					</div>
				</div>
				<div class="column2">
					<div class="col-md-4"> <!-- Centered Column -->
						<div class="panel panel-default" id="registrationPanel">
		  				<div class="panel-body">
								<form role="form" id="registrationForm" method="post" action="" autocomplete="on">
									<?php
									//check for any errors
									if(isset($error)){
										foreach($error as $error){
											echo '<p class="bg-danger">'.$error.'</p>';
										}
									}
									//if action is joined show sucess
									if(isset($_GET['action']) && $_GET['action'] == 'joined'){
										echo "<p class='bg-success' style='text-align:center;'><b>Hey thanks for signing up! Please check your email.</b><p>";
									}
									?>
									<div class="form-group formbox">
										<label>Username</label>
										<input type="text" name="username" id="username" class="form-control" placeholder="User Name" tabindex="1">
									</div>
									<div class="form-group formbox">
										<label>Email Address</label>
										<input type="email" name="EmailAddress" id="EmailAddress" class="form-control" placeholder="Email Address" tabindex="2">
									</div>
									<div class="form-group formbox">
										<label>Password</label>
										<input type="password" name="password" id="password" class="form-control" placeholder="Password" tabindex="3">
									</div>
									<div class="form-group formbox">
										<input type="password" name="passwordConfirm" id="passwordConfirm" class="form-control" placeholder="Confirm" tabindex="4">
									</div>
									<div class="form-group formbox">
										<label>Zipcode</label>
										<input type="text" name="Zipcode" class="form-control" id="Zipcode" placeholder="Zipcode (e.g. 20015)" tabindex="5">
									</div>
									<div class="form-group formbox">
										<label>Time Selection</label>
										<select name="time[]" data-max-options="2" data-min-options="2" tabindex="6" class="selectpicker" multiple>
											<optgroup label="Timezone">
												<option value="EDT">NY - Eastern Time</option>
												<option value="CDT">CHI - Central Time</option>
												<option value="MDT">TX - Mountain Time</option>
												<option value="PDT">CA - Pacific Time</option>
												<option value="AKDT">AK - Alaska Time</option>
												<option value="HST">HI - Hawaii Time</option>
											</optgroup>
											<optgroup label="Time">
												<option value="00:00:00">12:00am</option>
												<option value="00:30:00">12:30am</option>
												<option value="01:00:00">1:00am</option>
												<option value="01:30:00">1:30am</option>
												<option value="02:00:00">2:00am</option>
												<option value="02:30:00">2:30am</option>
												<option value="03:00:00">3:00am</option>
												<option value="03:30:00">3:30am</option>
												<option value="04:00:00">4:00am</option>
												<option value="04:30:00">4:30am</option>
												<option value="05:00:00">5:00am</option>
												<option value="05:30:00">5:30am</option>
												<option value="06:00:00">6:00am</option>
												<option value="06:30:00">6:30am</option>
												<option value="07:00:00">7:00am</option>
												<option value="07:30:00">7:30am</option>
												<option value="08:00:00">8:00am</option>
												<option value="08:30:00">8:30am</option>
												<option value="09:00:00">9:00am</option>
												<option value="09:30:00">9:30am</option>
												<option value="10:00:00">10:00am</option>
												<option value="10:30:00">10:30am</option>
												<option value="11:00:00">11:00am</option>
												<option value="11:30:00">11:30am</option>
												<option value="12:00:00">12:00pm</option>
												<option value="12:30:00">12:30pm</option>
												<option value="13:00:00">1:00pm</option>
												<option value="13:30:00">1:30pm</option>
												<option value="14:00:00">2:00pm</option>
												<option value="14:30:00">2:30pm</option>
												<option value="15:00:00">3:00pm</option>
												<option value="15:30:00">3:30pm</option>
												<option value="16:00:00">4:00pm</option>
												<option value="16:30:00">4:30pm</option>
												<option value="17:00:00">5:00pm</option>
												<option value="17:30:00">5:30pm</option>
												<option value="18:00:00">6:00pm</option>
												<option value="18:30:00">6:30pm</option>
												<option value="19:00:00">7:00pm</option>
												<option value="19:30:00">7:30pm</option>
												<option value="20:00:00">8:00pm</option>
												<option value="20:30:00">8:30pm</option>
												<option value="21:00:00">9:00pm</option>
												<option value="21:30:00">9:30pm</option>
												<option value="22:00:00">10:00pm</option>
												<option value="22:30:00">10:30pm</option>
												<option value="23:00:00">11:00pm</option>
												<option value="23:30:00">11:30pm</option>
											</optgroup>
										</select>
										<script type="text/javascript">$('.selectpicker').selectpicker({
												width: '100%',
										});</script>
									</div>
									<div class="form-actions">
										<input type="submit" name="submit" value="Sign Me Up!" class="btn btn-primary btn-lg btn-block" id="submitButton" tabindex="7">
										<a id="myAccount" href='login.php'>My Account</a>
									</div>								
								</form>
							</div>
							<div class="column3">
								<div class="col-md-4">
								</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
<div class="firstFrame">
	<h1>Stop searching for your weather. <b>Start getting it.</b></h1>
	<div class="row">
		<div class="column1">
			<div class="col-md-4" id="one">
			</div>
		</div>
		<div class="column2">
			<div class="col-md-4" id="two">
				<img src="img/iphone.gif" id="iPhone" align="middle">
			</div>
		</div>
		<div class="column3">
			<div class="col-md-4" id="three">
			</div>
		</div>
	</div>
	<div class="container-fluid">
		<span>
			<p>A <b>free</b> service that delivers weather to your inbox 
				each night so it's there waiting for you when you wake up.</p>
		</span>
	</div>
</div>
<div class="container-fluid" id="thirdframe-container">
	<div class="thirdFrame">
		<div class="container-fluid">
			<h1><b>Awesome</b> Data. <b>Awesome</b> Features.</h1>
		</div>
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-6">
					<ul>
						<li><b>We</b> get our weather from multiple providers so you can see who's forecasting what.</li>
						<li><b>We</b> then give you an average temperature to give you the most accurate weather prediction available.</li>
						<li>Hourly reports? Chance of rain? We've got it all.</li>
						<li>We even include an embedded <b>animated</b> radar map so you can see just how close that rain is before you embark on your morning commute.</li>
					</ul>
				</div>
				<div class="col-md-6">
					<img class="img-responsive" src="img/clouds_v1.svg">
				</div>
			</div>
		</div>
	</div>
</div>
<div class="container-fluid" id="providers-container">
	<div class="providers">
		<img class="img-responsive" src="img/weatherlogos.png" id="weatherLogos">
	</div>
</div>
<div class="container-fluid" id="forthframe-container">
	<div class="fourthFrame">
		<div class="container-fluid">
			<h1>We even <b>suggest what to wear</b>.</h1>
		</div>
		<br><br>
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-6">
					<img class="img-responsive" src="img/rain_clothing.svg">
				</div>
				<div class="col-md-6">
					<ul>
						<li id="unprepared"><b>Never be unprepared.</b></li>
						<li>Along with your weather report we send you accurate suggestions of what to wear for the day ahead.</li>
						<li><b>Don't worry,</b> we'll never let you leave the house without your umbrella.</b></li>
					</ul>
				</div>
			</div>
		</div>
		</div>
	</div>
</div>
<div class="container-fluid">
	<div class="fifthFrame">
		<div class="container-fluid">
			<h1>Like what you see?</h1>
			<p><a href="#toTop" onclick="$(#emailInput).focus();">Sign up, it's totally free!</a><p>
			<img class="img-responsive" src="img/cloudy_shoutout.svg">
		</div>
	</div>
</div>
<div class="footer">
	<div class="container">
		<p class="text-muted">Developed with <span class="redheart" style="font-size:120%;">&hearts;</span> by Grant McGovern</p>
		<p><a href="https://github.com/g12mcgov">github.com/g12mcgov</a></p>
	</div>
</div>

<?php 
//include header template
require('layout/footer.php'); 
?>
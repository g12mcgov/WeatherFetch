<?php require('includes/config.php'); 

/* INCLUDE HREF BACK TO THE HOME PAGEH */

//if not logged in redirect to login page
if(!$user->is_logged_in()){ header('Location: login.php'); } 

$username = $_SESSION['username'];

$stmt = $db->prepare("SELECT * FROM members WHERE username = :username");
$stmt->execute(array(':username' => $username));

$row = $stmt->fetch();

$memberID = $row['memberID'];
$EmailAddress = $row['EmailAddress'];
$Time = $row['Time'];
$Timezone = $row['Timezone'];
$Zipcode = $row['Zipcode'];

if(isset($_GET['delete'])){
	$stmt = $db->prepare("DELETE FROM members WHERE EmailAddress = :EmailAddress");
  $stmt->execute(array(':EmailAddress' => $EmailAddress));
  //logout
	$user->logout(); 
	//logged in return to index page
	header('Location: index.php');
	exit;
}

if(isset($_POST['time_change'])){
	$newTime = $_POST['time'];
	$Timezone = $newTime[0];
	$Time = $newTime[1];

	$stmt = $db->prepare("UPDATE members SET Timezone = :Timezone, Time = :Time WHERE EmailAddress = :EmailAddress");
  $stmt->execute(array(
  	':Timezone' => $Timezone,
  	':Time' => $Time,
  	':EmailAddress' => $EmailAddress
  	));

  echo "<p class='bg-success' id='changeSuccess' style='text-align:center;'><b>Time successfully changed.</b><p>";
}

if(isset($_POST['zipcode_change'])){
	$newZipcode = $_POST['Zipcode'];

	$stmt = $db->prepare("UPDATE members SET Zipcode = :Zipcode WHERE EmailAddress = :EmailAddress");
  $stmt->execute(array(
  	':Zipcode' => $newZipcode,
  	':EmailAddress' => $EmailAddress
  	));

  echo "<p class='bg-success' id='changeSuccess' style='text-align:center;'><b>Zipcode successfully changed.</b><p>";
}

//define page title
$title = 'My Account';

//include header template
require('layout/header.php'); 
?>

<div class="container-fluid">
	<div class="row">
			<div class="column_1">
		    <div class="col-md-4">
				</div>
			</div>
			<div class="column_2">
				<div class="col-md-4">
					<div class="logo">
					</div>
					<p><a href='logout.php' class="pull-right">Logout</a></p>
					<p><a href='index.php' class="pull-left">Home</a></p>
					<hr>
					<div class="panel panel-default">
  					<div class="panel-heading">
    					<h3 class="panel-title">Username</h3>
  					</div>
  					<div class="panel-body">
    					<p><?php echo $username ?></p>
  					</div>
					</div>
					<div class="panel panel-default">
  					<div class="panel-heading">
    					<h3 class="panel-title">Email</h3>
  					</div>
  					<div class="panel-body">
    					<p><?php echo $EmailAddress ?>
  					</div>
					</div>
					<div class="panel panel-default">
  					<div class="panel-heading">
    					<h3 class="panel-title">Time</h3>
  					</div>
  					<div class="panel-body">
    					<p><?php echo $Time ?></p>
  					</div>
					</div>
					<div class="panel panel-default">
  					<div class="panel-heading">
    					<h3 class="panel-title">Timezone</h3>
  					</div>
  					<div class="panel-body">
    					<p><?php echo $Timezone ?></p>
  					</div>
					</div>
					<div class="panel panel-default">
  					<div class="panel-heading">
    					<h3 class="panel-title">Zipcode</h3>
  					</div>
  					<div class="panel-body">
    					<p><?php echo $Zipcode ?></p>
  					</div>
					</div>
					<div class="centered">
						<a href="#ChangeTime" data-toggle="modal" data-target="#ChangeTime">Change Your Time</a>
					</div>
					<div class="modal fade" id="ChangeTime">
						<div class="modal-dialog">
	    				<div class="modal-content">
	      				<div class="modal-header">
	        				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
	        				<h4 class="modal-title">Select Your New Time</h4>
	      				</div>
	      				<div class="modal-body">
	        				<form role="form" id="timeSelect" method="post" action="" autocomplete="on">
										<div class="form-group formbox">
											<label>Time Selection</label>
											<select name="time[]" data-max-options="2" tabindex="1" class="selectpicker" multiple>
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
											<input type="submit" name="time_change" value="Submit" class="btn btn-primary btn-lg btn-block" id="submitButton" tabindex="2">
										</div>								
									</form>
	      				</div>
	    				</div>
	  				</div>
					</div>
					<div class="centered">
						<a href="#ChangeZipcode" data-toggle="modal" data-target="#ChangeZipcode">Change Your Zipcode</a>
					</div>
					<div class="modal fade" id="ChangeZipcode">
						<div class="modal-dialog">
	    				<div class="modal-content">
	      				<div class="modal-header">
	        				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
	        				<h4 class="modal-title">Enter Your New Zipcode</h4>
	      				</div>
	      				<div class="modal-body">
	        				<form role="form" id="Zipcode" method="post" action="" autocomplete="on">
										<div class="form-group formbox">
											<label>Zipcode</label>
											<div class="form-group formbox">
												<input type="text" name="Zipcode" class="form-control" id="Zipcode" placeholder="Zipcode (e.g. 20015)" tabindex="5">
											</div>
										</div>
										<div class="form-actions">
											<input type="submit" name="zipcode_change" value="Submit" class="btn btn-primary btn-lg btn-block" id="submitButton" tabindex="2">
										</div>								
									</form>
	      				</div>
	    				</div>
	  				</div>
					</div>
					<div class="centered">
						<a class="btn btn-danger" onclick="return confirm('Oh no! Are you sure you want to go?')" id="deleteAccount" href='memberpage.php?delete=true'>Delete Account</a>
					</div>
					<script src="../loginregister/js/TimeSuccess.js"></script>
				</div> <!-- End Middle Column -->
			</div>
			<div class="column_3">
				<div class="col-md-4">
				</div>
			</div>
	</div>
</div>

<?php 
require('layout/footer.php'); 
?>
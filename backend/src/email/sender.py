
import os
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from body import * ## Import email body
script_dir = sys.path[0]
img_path = os.path.join(script_dir, 'email/img/WeatherFetchLogo.png')

def sendEmail(email_body):
	print "sending email"
	# Define these once; use them twice!
	strFrom = 'grantmcgovern.mcgovern@gmail.com'
	strTo = 'mcgoga12@wfu.edu'

	# Create the root message and fill in the from, to, and subject headers
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'test message'
	msgRoot['From'] = strFrom
	msgRoot['To'] = strTo
	msgRoot.preamble = 'This is a multi-part message in MIME format.'

	# Encapsulate the plain and HTML versions of the message body in an
	# 'alternative' part, so message agents can decide which they want to display.
	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	msgText = MIMEText('This is the alternative plain text message.')
	msgAlternative.attach(msgText)

	# We reference the image in the IMG SRC attribute by the ID we give it below
	msgText = MIMEText(email_body, 'html')
	msgAlternative.attach(msgText)

	# This example assumes the image is in the current directory
	fp = open(img_path, 'rb')
	msgImage = MIMEImage(fp.read())
	fp.close()

	# Define the image's ID as referenced above
	msgImage.add_header('Content-ID', '<logo>')
	msgRoot.attach(msgImage)

	# Send the email (this example assumes SMTP authentication is required)
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login('grantmcgovern.mcgovern@gmail.com', 'grantmcgovern1')
		server.sendmail(strFrom, strTo, msgRoot.as_string())
		server.close()
	except:
		print "Could not send email."


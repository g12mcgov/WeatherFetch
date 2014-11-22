#!/usr/local/bin/python

##
## WeatherFetch - GROUPS.
## 
## **** THIS FILE SENDS THE ACTUAL EMAIL ***  
## 
## Created by: Grant McGovern
## Date: 18 August 2014
## Contact: github.com/g12mcgov 
##
## Purpose: Using the HTML email body, this packages and sends the email.
##
##
##

import os
import sys
import time
import smtplib
from email import message_from_file 
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
## Local Includes ## 
from body import constructTemplate 
script_dir = sys.path[0]
img_path = os.path.join(script_dir, 'email/img/WeatherFetchLogo.png')

def sendEmail(email_body, icon_path):
	print "Sending email..."
	strFrom = 'grantmcgovern.mcgovern@gmail.com'
	strTo = 'jamesbroyce@gmail.com'

	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Your Daily Report for %s' % (time.strftime("%m/%d/%Y"))
	msgRoot['From'] = strFrom
	msgRoot['To'] = strTo

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	msgText = MIMEText('This is the alternative plain text message.')
	msgAlternative.attach(msgText)

	msgText = MIMEText(email_body, 'html')
	msgAlternative.attach(msgText)

	fp = open(img_path, 'rb')
	logo_image = MIMEImage(fp.read())

	fp = open(str(icon_path), 'rb')
	icon_image = MIMEImage(fp.read())

	fp.close()

	## Associate images with their respective content
	logo_image.add_header('Content-ID', '<logo>')
	icon_image.add_header('Content-ID', '<icon>')
	
	msgRoot.attach(icon_image)
	msgRoot.attach(logo_image)

	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		try:
			server.login('##', '##')
		except SMTPAuthenticationError:
			server.quit()
			raise Exception("Invalid credentials - could not authenticate")
		server.sendmail(strFrom, strTo, msgRoot.as_string())
		server.close()
		print "Email successfully sent."
	except:
		raise Exception("Email could not be sent")


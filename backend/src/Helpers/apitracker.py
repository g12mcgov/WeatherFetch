##
## WeatherFetch - DB.
## 
## **** THIS FILE HANDLES DATABASE WORK ***  
## 
## Created by: Grant McGovern
## Date: 31 July 2014
## Contact: github.com/g12mcgov 
##
## Purpose: Connect to MySQL DB running on Amazon EC2 instance
##
##
##

from twilio.rest import TwilioRestClient

def apiLimiter(expected_api_calls):
	if expected_api_calls > 200:
		apiAlert("Wunderground API's exceeded (200 calls)")
	elif expected_api_calls > 500:
		apiAlert("WorldWeather API's exceeded (500 calls)")
	elif expected_api_calls > 10000:
		apiAlert("Forecast.io API's exceeded (10,000 calls")

def apiAlert(message):
	account_sid = "AC7c7baa3c88f18a243b2c81594c7746ad"
	auth_token = "245cf1a14c233c80cfbbe27a3c5d10c2"
	client = TwilioRestClient(account_sid, auth_token)
 
	message = client.messages.create(to="+13016533550", from_="+16364870116", body=message)
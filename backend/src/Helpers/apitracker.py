##
## WeatherFetch - APITRACKER.py.
## 
## **** THIS FILE TRACKS API USAGE AND NOTIFIES IF SPILLOVER ***  
## 
## Created by: Grant McGovern
## Date: 18 August 2014
## Contact: github.com/g12mcgov 
##
## Purpose: Using Twilio, if API requests exceeded defined limits, it notifies me via SMS. 
## 			Handy way to know when to bump up usage.
##
##
##

from twilio.rest import TwilioRestClient

def apiLimiter(expected_api_calls):
	if expected_api_calls > 200:
		apiAlert("Wunderground API's exceeded (200 calls)")
	elif expected_api_calls > 500:
		apiAlert("WorldWeather API's exceeded (500 calls)")
	elif expected_api_calls > 1000:
		apiAlert("Forecast.io API's exceeded (1,000 calls")

def apiAlert(message):
	account_sid = "AC7c7baa3c88f18a243b2c81594c7746ad"
	auth_token = "245cf1a14c233c80cfbbe27a3c5d10c2"
	client = TwilioRestClient(account_sid, auth_token)
 
	message = client.messages.create(to="+13016533550", from_="+16364870116", body=message)


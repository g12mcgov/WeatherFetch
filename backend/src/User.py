##
## WeatherFetch - GROUPS.
## 
## **** THIS FILE DESCRIBES STRUCTURE FOR USERS ***  
## 
## Created by: Grant McGovern
## Date: 31 July 2014
## Contact: github.com/g12mcgov 
##
## Purpose: Define the class structure for User objects.
##
##
##

class User():
	def __init__(self, userId, username, emailAddress, time, timezone, zipcode, ForecastIO, WunderGround, WorldWeather): ## weather is an object
		self.userId = userId
		self.username = username
		self.emailAddress = emailAddress
		self.time = time
		self.timezone = timezone
		self.zipcode = zipcode
		self.ForecastIO = ForecastIO
		self.WunderGround = WunderGround
		self.WorldWeather = WorldWeather

	def getUserId(self):
		return self.userId

	def getUsername(self):
		return self.username

	def getEmailAddress(self):
		return self.emailAddress

	def getTime(self):
		return self.time

	def getTimezone(self):
		return self.timezone

	def getZipcode(self):
		return self.zipcode

	def getForecastIO(self):
		return self.ForecastIO

	def getAggregateWeather(self):
		pass

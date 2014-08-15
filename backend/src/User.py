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
import json 

class User():
	def __init__(self, userId, username, emailAddress, time, timezone, zipcode, ForecastIO, WunderGround, HamWeather): ## weather is an object
		self.userId = userId
		self.username = username
		self.emailAddress = emailAddress
		self.time = time
		self.timezone = timezone
		self.zipcode = zipcode
		self.ForecastIO = ForecastIO
		self.WunderGround = WunderGround
		self.HamWeather = HamWeather

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

	## These will return as dicts
	def getForecastIORaw(self):
		return self.ForecastIO

	## These will return as dicts
	def getWundergroundRaw(self):
		return self.WunderGround

	## These will return as dicts
	def getHamWeatherRaw(self):
		return self.HamWeather

	def getAggregateWeather(self):
		return (self.ForecastIO, self.WunderGround, self.HamWeather)

	def getWeatherMap(self):
		data = self.WunderGround
		weather_map = data[2]['weather_map']

		return weather_map

	def hourlyForecastIO(self):
		hourly_data = self.ForecastIO[0]
		general = hourly_data[0]['general']
		overall_icon = general['overall_icon']
		overall_summary = general['overall_summary']
		
		## Remove General field that we previously appended ## 
		del(hourly_data[0])

		formatted_hours = []

		hours = hourly_data
		number_of_hours = len(hours)

		for hour in hours:
			time = hour['time'].lstrip('0')+': ' # Get rid of leading '0'
			temp = str(hour['temperature'])+'F'
			pop = str(int(hour['precipProbability']*100))+'%' # Get rid of decimal, make string to append '%'
			group = lambda time, temp, pop: (time, temp, pop) # Make tuples
			formatted_hours.append(group(time, temp, pop))

		return (overall_icon, overall_summary, formatted_hours)

	def hourlyWunderGround(self):
		hourly_data = self.WunderGround[1]

		formatted_hours = []

		hours = hourly_data
		
		for hour in hours:
			time = hour['time']
			temp = hour['temp']+'F'
			pop = hour['precipProbability']+'%'
			group = lambda time, temp, pop: (time, temp, pop)
			formatted_hours.append(group(time, temp, pop))

		
		return formatted_hours

	def hourlyHamWeather(self):
		hourly_data = self.HamWeather[1]

		formatted_hours = []

		hours = hourly_data

		for hour in hours:
			time = hour['time'].lstrip('0')+': '
			temp = str(hour['temp'])+'F'
			pop = str(hour['pop'])+'%'
			group = lambda time, temp, pop: (time, temp, pop)
			formatted_hours.append(group(time, temp, pop))


		return formatted_hours





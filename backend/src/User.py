##
## WeatherFetch - USER.py.
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

	def currentForecastIO(self):
		current_data = self.ForecastIO[1]
		
		## Extract from dict ## 
		forecast_ioDict = {}
		forecast_ioDict['temperature'] = current_data['temperature']
		forecast_ioDict['summary'] = current_data['summary']
		forecast_ioDict['time'] = current_data['time']
		forecast_ioDict['pop'] = str(current_data['precipProbability'])+'%'
		forecast_ioDict['humidity'] = current_data['humidity']
		forecast_ioDict['tempMax'] = current_data['tempMax']
		forecast_ioDict['tempMin'] = current_data['tempMin']

		return forecast_ioDict

	def currentWunderGround(self):
		current_data = self.WunderGround[0]
		
		## Extract from dict ##
		wundergroundDict = {}
		wundergroundDict['temperature'] = current_data['temp_f']
		wundergroundDict['summary'] = current_data['weather']
		wundergroundDict['time'] = current_data['local_time_rfc822']
		wundergroundDict['pop'] = str(current_data['pop'])+'%'
		wundergroundDict['humidity'] = current_data['relative_humidity']
		wundergroundDict['tempMax'] = current_data['maxTemp']
		wundergroundDict['tempMin'] = current_data['minTemp']

		return wundergroundDict

	def currentHamWeather(self):
		current_data = self.HamWeather[0]
		
		hamweatherDict = {}
		hamweatherDict['temperature'] = current_data['temp']
		hamweatherDict['summary'] = current_data['weather']
		hamweatherDict['time'] = current_data['time']
		hamweatherDict['pop'] = str(current_data['pop'])+'%'
		hamweatherDict['humidity'] = str(current_data['humidity'])+'%'
		hamweatherDict['tempMax'] = current_data['maxTemp']
		hamweatherDict['tempMin'] = current_data['minTemp']

		return hamweatherDict

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
			temp = str(hour['temperature'])
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
			temp = hour['temp']
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
			temp = str(hour['temp'])
			pop = str(hour['pop'])+'%'
			group = lambda time, temp, pop: (time, temp, pop)
			formatted_hours.append(group(time, temp, pop))


		return formatted_hours

	def hourlyAverage(self):
		hamweather = self.HamWeather[1]
		wunderground = self.WunderGround[1]
		forecast_io = self.ForecastIO[0]

		print json.dumps(forecast_io, separators=(',',':'), indent=4)

		## Some of my more proud work... ##

		## Using list comprehension for speed!!!!! ##
		## HamWeather Lists ## 
		hamWeatherTemps = [float(temp['temp']) for temp in hamweather]
		hamWeatherPops = [float(pop['pop']) for pop in hamweather]
		## Forecast.io Lists ##
		forecastioTemps = [float(temp['temperature']) for temp in forecast_io]
		forecastioPops = [float(pop['precipProbability']) for pop in forecast_io]
		## WunderGround Lists ## 
		wundergroundTemps = [float(temp['temp']) for temp in wunderground]
		wundergroundPops = [float(pop['precipProbability']) for pop in wunderground]

		## Use an arbitrary set for time, they're all the same.
		times = [str(time['time']).lstrip('0')+': ' for time in hamweather]

		average = lambda nums, default=float('nan'): (sum(nums)/float(len(nums))) if nums else default
		
		average_temps = [round(average(n), 1) for n in zip(hamWeatherTemps, forecastioTemps, wundergroundTemps)]
		average_pops = [round(average(n), 1) for n in zip(hamWeatherPops, forecastioPops, wundergroundPops)]

		hourly_averages = [(time, temp, pop) for time, temp, pop in zip(times, average_temps, average_pops)]

		return hourly_averages

	def computeCurrentAverage(self):
		wunderground_temp = float(self.WunderGround[0]['temp_f']) ## Current info stored in index[0]
		forecast_io_temp = float(self.ForecastIO[1]['temperature']) ## Current info stored in index[1]
		hamweather_temp = float(self.HamWeather[0]['temp']) ## Current info stored in index[0]

		avg = lambda wunderground_temp, forecast_io_temp, hamweather_temp: round(((wunderground_temp+forecast_io_temp+hamweather_temp)/3), 1)
		average = avg(wunderground_temp, forecast_io_temp, hamweather_temp)


		return average

	def computeMaxAverage(self):
		wunderground_max = float(self.WunderGround[0]['maxTemp']) ## Current info stored in index[0]
		forecast_io_max = float(self.ForecastIO[1]['tempMax']) ## Current info stored in index[1]
		hamweather_max = float(self.HamWeather[0]['maxTemp']) ## Current info stored in index[0]

		avg = lambda wunderground_max, forecast_io_max, hamweather_max: round(((wunderground_max+forecast_io_max+hamweather_max)/3), 1)
		average = avg(wunderground_max, forecast_io_max, hamweather_max)


		return average

	def computeMinAverage(self):
		wunderground_min = float(self.WunderGround[0]['minTemp']) ## Current info stored in index[0]
		forecast_io_min = float(self.ForecastIO[1]['tempMin']) ## Current info stored in index[1]
		hamweather_min = float(self.HamWeather[0]['minTemp']) ## Current info stored in index[0]

		avg = lambda wunderground_min, forecast_io_min, hamweather_min: round(((wunderground_min+forecast_io_min+hamweather_min)/3), 1)
		average = avg(wunderground_min, forecast_io_min, hamweather_min)


		return average

	def currentPOP(self):
		wunderground_current = float(self.WunderGround[0]['pop']) ## Current info stored in index[0]
		forecast_io_current = float(self.ForecastIO[1]['precipProbability']) ## Current info stored in index[1]
		hamweather_current = float(self.HamWeather[0]['pop']) ## Current info stored in index[0]

		avg = lambda wunderground_current, forecast_io_current, hamweather_current: round(((wunderground_current+forecast_io_current+hamweather_current)/3), 1)
		average = str(avg(wunderground_current, forecast_io_current, hamweather_current))+'%'		
		

		return average






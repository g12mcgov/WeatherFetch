##
## WeatherFetch - MAIN.
## 
## **** THIS FILE IS THE DRIVER ***  
## 
## Created by: Grant McGovern
## Date: 31 July 2014
## Contact: github.com/g12mcgov 
##
## Purpose: This is the main driver for the entire application.
##
##
##

import os
import sys
import inspect
import logging
import requests
import multiprocessing
## Local Includes 
sys.path.append('weather')
sys.path.append('helpers')
sys.path.append('Email')
## 
from Database import *
from forecast import *
from wunderground import *
from hamweather import *
from user import User
from apitracker import apiLimiter, apiAlert
from body import constructTemplate
from sender import sendEmail
from suggestions import suggestion

## Define Timezone ## 
TIME_ZONE = "EDT"

def main():
	CPU_COUNT = multiprocessing.cpu_count()
	pool = multiprocessing.Pool(processes=CPU_COUNT-1)

	cursor = establishDBConnection()
	members = getDBData(cursor, TIME_ZONE)
	userDicts = createUserDict(members)

	users_with_weather = pool.map(aggregateWeatherGrab, userDicts)

	Users = createUsers(users_with_weather)

	expected_api_calls = (len(Users) * 5)
	apiLimiter(expected_api_calls)

	for user in Users:
		## Current Data ##
		forecast_io_current = user.currentForecastIO()
		wunderground_current = user.currentWunderGround()
		hamweather_current = user.currentHamWeather()
		## Hourly Data ##
		forecast_io_hourly = user.hourlyForecastIO()
		wunderground_hourly = user.hourlyWunderGround()
		hamweather_hourly = user.hourlyHamWeather()
		average_hourly = user.hourlyAverage()
		## Weather Map ##
		weather_map = user.getWeatherMap()
		## Averages ##
		current_average = user.computeCurrentAverage()
		max_average = user.computeMaxAverage()
		min_average = user.computeMinAverage()
		## Precipitation ##
		pop = user.currentPOP()
		## Make Suggestions ##
		suggestions = suggestion(forecast_io_hourly, current_average, max_average, min_average, pop)
		
		## Construct email and send. If we get enough users, this will be switched to send batch messages 
		## at once, most likely through an API (mailchimp) or using postfix.
		email_body = constructTemplate(forecast_io_current, wunderground_current, hamweather_current, 
			forecast_io_hourly, wunderground_hourly, hamweather_hourly, weather_map, current_average, 
			max_average, min_average, pop)
		
		sendEmail(email_body)

def createUserDict(members):
	userDicts = []
	for user in members:
		userDict = {}
		formatted_time = str(user[4])
		userDict['userId'] = user[0] 
		userDict['username'] = user[1]
		userDict['email'] = user[3]
		userDict['time'] = formatted_time
		userDict['timezone'] = user[5]
		userDict['zipcode'] = user[6]
		userDicts.append(userDict)

	return userDicts

def createUsers(users_with_weather):
	Users = []
	for userDict in users_with_weather:
		userId = userDict['userId']
		username = userDict['username']
		email = userDict['email']
		time = userDict['time']
		timezone = userDict['timezone']
		zipcode = userDict['zipcode']
		## WEATHER ##
		forecast_io = userDict['forecastIo']
		wunderground = userDict['wunderground']
		hamweather = userDict['hamweather']

		Users.append(User(userId, username, email, time, timezone, zipcode, forecast_io, wunderground, hamweather))

	return Users


def aggregateWeatherGrab(userDicts):
	zipcodes = userDicts['zipcode']
	forecast_io = forecastIO(zipcodes)
	wunderground = wunderGround(zipcodes)
	hamweather = hamWeather(zipcodes)

	userDicts['forecastIo'] = forecast_io
	userDicts['wunderground'] = wunderground
	userDicts['hamweather'] = hamweather

	#apiCount(wunderGround.count, hamWeather.count, forecastIO.count)

	return userDicts

def apiCount(wunderground_count, hamweather_count, forecast_io_count):
	wunderground_count_list = []
	hamweather_count_list = []
	forecast_io_count_list = []

	wunderground_count_list.append(wunderground_count)
	hamweather_count_list.append(hamweather_count)
	forecast_io_count_list.append(forecast_io_count)

	wunder_sum = sum(wunderground_count_list)
	ham_sum = sum(hamweather_count_list)
	forecast_sum = sum(forecast_io_count_list)

	#print wunder_sum
	#print ham_sum
	#print forecast_sum


if __name__ == "__main__":
	main()
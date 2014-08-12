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
import multiprocessing

sys.path.append('Weather')
sys.path.append('Helpers')
## Local Includes 
from Database import *
from forecast import *
from wunderground import *
from worldweather import *
from User import *
from apitracker import *

def main():
	CPU_COUNT = multiprocessing.cpu_count()
	pool = multiprocessing.Pool(processes=CPU_COUNT-1)

	cursor = establishDBConnection()
	members = getDBData(cursor)
	userDicts = createUserDict(members)

	users_with_weather = pool.map(aggregateWeatherGrab, userDicts)

	Users = createUsers(users_with_weather)

	expected_api_calls = (len(Users) * 5)
	apiLimiter(expected_api_calls)

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
		#print json.dumps(userDict, separators=(',',':'), indent=4)
		userId = userDict['userId']
		username = userDict['username']
		email = userDict['email']
		time = userDict['time']
		timezone = userDict['timezone']
		zipcode = userDict['zipcode']
		## WEATHER ##
		forecast_io = userDict['forecastIo']
		wunderground = userDict['wunderground']

		Users.append(User(userId, username, email, time, timezone, zipcode, forecast_io, wunderground, None))

	return Users


def aggregateWeatherGrab(userDicts):
	zipcodes = userDicts['zipcode']
	forecast_io = forecastIO(zipcodes)
	wunderground = wunderGround(zipcodes)
	worldweather = worldWeather(zipcodes)

	userDicts['forecastIo'] = forecast_io
	userDicts['wunderground'] = wunderground
	userDicts['worldweather'] = worldweather

	return userDicts

if __name__ == "__main__":
	main()
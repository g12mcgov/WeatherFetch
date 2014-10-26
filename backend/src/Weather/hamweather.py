#!/usr/local/bin/python	

##
## WeatherFetch - Hamweather.py
## 
## **** THIS FILE IS DESIGNED TO OBTAIN DATA FROM HAMWEATHER ***  
## 
## Created by: Grant McGovern
## Date: 31 July 2014
## Contact: github.com/g12mcgov 
##
## Purpose: Hits Hamweather.com API and recieves data for the rest of the application
##
##
##

import json
import requests
import time
import os.path
import itertools
import datetime
import operator	
from wrappers import * 

CONSUMER_ID = '#'
CONSUMER_SECRET = '#'
BASE_URL = 'http://api.aerisapi.com/'

@counter
def hamWeather(zipcodes):
	hourly = getHourlyWeather(zipcodes)
	current = getCurrentWeather(zipcodes)
	data = processData(current, hourly)

	return data 


def getHourlyWeather(zipcodes):
	params = {'client_id':CONSUMER_ID, 'client_secret':CONSUMER_SECRET, 'filter':'1hr'}
	hourly = json.loads(requests.get(url=BASE_URL+'forecasts/'+zipcodes, params=params).content)

	save_path = 'Weather/responses/'
	complete_path = save_path + 'hamweather_hourly.js'
	
	#with open(complete_path, "wb") as outfile:
	#	outfile.write(json.dumps(hourly, separators=(',',':'), indent=4))

	return hourly


def getCurrentWeather(zipcodes):
	params = {'client_id':CONSUMER_ID, 'client_secret':CONSUMER_SECRET}
	current = json.loads(requests.get(url=BASE_URL+'observations/'+zipcodes, params=params).content)

	save_path = 'Weather/responses/'
	complete_path = save_path + 'hamweather_current.js'
	
	#with open(complete_path, "wb") as outfile:
	#	outfile.write(json.dumps(current, separators=(',',':'), indent=4))

	return current

def processData(current, hourly):
	## Hourly ##
	hourly_weather = hourly['response'][0] # They return response as a list... with 1 item. Stupid. Forces us to index.
	periods = hourly_weather['periods']

	max_temps = []
	hourlyDictList = []
	for hour in itertools.islice(periods, 0, 10): # Only grab the first 10 hours
		hourlyDict = {}
		hourlyDict['pop'] = hour['pop']
		hourlyDict['avgTemp'] = hour['avgTempF']
		hourlyDict['weather'] = hour['weather']
		hourlyDict['snowDepth'] = hour['snowIN']
		hourlyDict['minTemp'] = hour['minTempF']
		hourlyDict['maxTemp'] = hour['maxTempF']
		hourlyDict['time'] = datetime.datetime.fromtimestamp(int(hour['timestamp'])).strftime('%I:%M %p')
		hourlyDict['temp'] = hour['tempF']
		hourlyDict['humidity'] = hour['humidity']
		hourlyDict['icon'] = hour['icon']
		hourlyDictList.append(hourlyDict)

	## Create a list of max temps and find the highest temperature in it
	max_temps = [temp['maxTemp'] for temp in hourlyDictList]
	index, max_temp = max(enumerate(max_temps), key=operator.itemgetter(1))

	## Create a list of min temps and find the lowest temperature in it
	min_temps = [temp['minTemp'] for temp in hourlyDictList]
	index, min_temp = min(enumerate(min_temps), key=operator.itemgetter(1))

	## Current ## 
	current_weather = current['response']
	current_object = current_weather['ob']


	currentDict = {}
	currentDict['maxTemp'] = str(max_temp)
	currentDict['minTemp'] = str(min_temp)
	currentDict['weatherPrimary'] = current_object['weatherPrimary']
	currentDict['weather'] = current_object['weather']
	currentDict['sunrise'] = datetime.datetime.fromtimestamp(int(current_object['sunrise'])).strftime('%I:%M %p')
	currentDict['icon'] = current_object['icon']
	currentDict['time'] = datetime.datetime.fromtimestamp(int(current_object['timestamp'])).strftime('%I:%M %p')
	print current_object['tempF']
	currentDict['temp'] = current_object['tempF']
	currentDict['snowDepth'] = current_object['snowDepthIN']
	currentDict['humidity'] = current_object['humidity']
	currentDict['pop'] = hourlyDictList[0]['pop'] # Oddly doesn't return pop for current weather so we steal from hour 1 of above data

	data = tuple([currentDict, hourlyDictList])

	return data















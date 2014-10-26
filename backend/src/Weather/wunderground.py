#!/usr/local/bin/python

##
## WeatherFetch - MAIN.
## 
## **** THIS FILE IS DESIGNED TO OBTAIN DATA FROM WEATHERUNDERGROUND ***  
## 
## Created by: Grant McGovern
## Date: 31 July 2014
## Contact: github.com/g12mcgov 
##
## Purpose: Hits Wunderground.com API and recieves data for the rest of the application
##
##
##

import json 
import requests
import datetime
import itertools
import urllib
import urlparse
import operator
from wrappers import * 

API_KEY = '#'
BASE_URL = '#'

@counter
def wunderGround(zipcodes):
	current_weather = getCurrentWeather(zipcodes)
	hourly_weather = getHourlyForecast(zipcodes)
	weather_map = getWeatherMap(zipcodes)
	data = processData(current_weather, hourly_weather, weather_map)

	return data
	
def getCurrentWeather(zipcodes):
	current_weather = json.loads(requests.get(url=BASE_URL+API_KEY+'/conditions/q/'+zipcodes+'.json').content)

	save_path = 'Weather/responses/'
	complete_path = save_path + 'wunderground_current.js'
	
	#with open(complete_path, "wb") as outfile:
	#	outfile.write(json.dumps(current_weather, separators=(',',':'), indent=4))
	
	return current_weather

def getHourlyForecast(zipcodes):
	hourly_weather = json.loads(requests.get(url=BASE_URL+API_KEY+'/hourly/q/'+zipcodes+'.json').content)

	save_path = 'Weather/responses/'
	complete_path = save_path + 'wunderground_hourly.js'
	
	#with open(complete_path, "wb") as outfile:
	#	outfile.write(json.dumps(hourly_weather, separators=(',',':'), indent=4))

	return hourly_weather

def getWeatherMap(zipcodes):
	url = BASE_URL+API_KEY+'/animatedradar/q/'+zipcodes+'.gif'
	params = {'newmaps':'1', 'timelabel':'1', 'timelabel.y':'10', 'num':'5', 'delay':'15'}
	
	url_parts = list(urlparse.urlparse(url))
	query = dict(urlparse.parse_qsl(url_parts[4]))
	query.update(params)
	
	url_parts[4] = urllib.urlencode(query)
	
	weather_map = urlparse.urlunparse(url_parts)

	return weather_map

def processData(current_weather, hourly_weather, weather_map):
	## Hourly ## 

	hourly_forecast = hourly_weather['hourly_forecast']
	hourlyDictList = []

	for hour in itertools.islice(hourly_forecast, 0, 10): ## Only grab the next 10 hours
		hourlyDict = {}
		hourlyDict['temp'] = hour['temp']['english']
		hourlyDict['humidity'] = hour['humidity']
		hourlyDict['time'] = hour['FCTTIME']['civil']
		hourlyDict['GMT_time'] = datetime.datetime.fromtimestamp(int(hour['FCTTIME']['epoch'])).strftime('%H:%M')
		hourlyDict['pretty_time'] = hour['FCTTIME']['pretty']
		hourlyDict['condition'] = hour['condition']
		hourlyDict['icon'] = hour['icon']
		hourlyDict['precipProbability'] = hour['pop']
		hourlyDictList.append(hourlyDict)

	## Current ## 
	current_observation = current_weather['current_observation']

	temps = [temp['temp'] for temp in hourlyDictList]
	## Calculate max temp
	index, max_temp = max(enumerate(temps), key=operator.itemgetter(1))
	## Calculate min temp
	index, min_temp = min(enumerate(temps), key=operator.itemgetter(1))

	currentDict = {}
	currentDict['pop'] = hourlyDictList[0]['precipProbability']
	currentDict['maxTemp'] = max_temp
	currentDict['minTemp'] = min_temp
	currentDict['weather'] = current_observation['weather']
	currentDict['local_time_rfc822'] = current_observation['local_time_rfc822']
	currentDict['precip_today_string'] = current_observation['precip_today_string']
	currentDict['precip_today_metric'] = current_observation['precip_today_metric']
	currentDict['precip_today_in'] = current_observation['precip_today_in']
	currentDict['temp_f'] = current_observation['temp_f']
	currentDict['icon'] = current_observation['icon']
	currentDict['relative_humidity'] = current_observation['relative_humidity']

	weatherDict = {'weather_map':weather_map}

	data = tuple([currentDict, hourlyDictList, weatherDict])

	return data






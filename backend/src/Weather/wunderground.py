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

API_KEY = '8bb93b6670e3f3de'
BASE_URL = 'http://api.wunderground.com/api/'


def wunderGround(zipcodes):
	current_weather = getCurrentWeather(zipcodes)
	hourly_weather = getHourlyForecast(zipcodes)
	weather_map = getWeatherMap(zipcodes)
	data = processData(current_weather, hourly_weather, weather_map)

	return data
	

def getCurrentWeather(zipcodes):
	current_weather = json.loads(requests.get(url=BASE_URL+API_KEY+'/conditions/q/'+zipcodes+'.json').content)

	with open("wunderground_current.js", "wb") as outfile:
		outfile.write(json.dumps(current_weather, separators=(',',':'), indent=4))

	#print json.dumps(current_weather, separators=(',',':'), indent=4)
	
	return current_weather

def getHourlyForecast(zipcodes):
	hourly_weather = json.loads(requests.get(url=BASE_URL+API_KEY+'/hourly/q/'+zipcodes+'.json').content)

	with open("wunderground_hourly.js", "wb") as outfile:
		outfile.write(json.dumps(hourly_weather, separators=(',',':'), indent=4))
	
	#print json.dumps(hourly_weather, separators=(',',':'), indent=4)

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
	## Current ## 
	current_observation = current_weather['current_observation']

	currentDict = {}
	currentDict['weather'] = current_observation['weather']
	currentDict['local_time_rfc822'] = current_observation['local_time_rfc822']
	currentDict['precip_today_string'] = current_observation['precip_today_string']
	currentDict['precip_today_metric'] = current_observation['precip_today_metric']
	currentDict['precip_today_in'] = current_observation['precip_today_in']
	currentDict['temp_f'] = current_observation['temp_f']
	currentDict['icon'] = current_observation['icon']
	currentDict['relative_humidity'] = current_observation['relative_humidity']

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

	weatherDict = {'weather_map':weather_map}

	data = tuple([currentDict, hourlyDictList, weatherDict])

	return data






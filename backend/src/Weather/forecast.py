##
## WeatherFetch - FORECAST.py.
## 
## **** THIS FILE GETS WEATHER DATA FROM Forecast.io ***  
## 
## Created by: Grant McGovern
## Date: 31 July 2014
## Contact: github.com/g12mcgov 
##
## Purpose: To fetch weather data from Forecast.io.
##
##
##

import json 
import requests
import datetime
from pyzipcode import ZipCodeDatabase
import itertools 
from wrappers import * 

API_KEY = '4dd221246d2daff383469cf4a5b68b32/'
BASE_URL = 'https://api.forecast.io/forecast/'

@counter
def forecastIO(zipcode):
	geoDict = zipcodeConverter(zipcode)
	response = outboundCall(geoDict)
	data = processData(response)

	return data

def zipcodeConverter(zipcode):
	## May need to look at performance issues here.
	zipcode_db = ZipCodeDatabase()
	response = zipcode_db[zipcode]

	city = response.city
	state = response.state
	longitude = response.longitude
	latitude = response.latitude
	
	geoDict = {}
	geoDict['city'] = city
	geoDict['state'] = state
	geoDict['longitude'] = longitude
	geoDict['latitude'] = latitude

	return geoDict 


def outboundCall(geoDict):
	longitude = geoDict['longitude']
	latitude = geoDict['latitude']

	response = json.loads(requests.get(url=BASE_URL+API_KEY+str(latitude)+','+str(longitude)).content)

	#print json.dumps(response, separators=(',',':'), indent=4)

	return response 


def processData(response):
	hourly_data = response['hourly']

	icon = hourly_data['icon']
	summary = hourly_data['summary']

	hourly = [data for data in hourly_data['data']]

	hourlyDictList = []
	hourlyDictList.append({'general':{'overall_icon':icon, 'overall_summary':summary}})

	for hour in itertools.islice(hourly, 0, 10):
		hourlyDict = {}
		hourlyDict['time'] = datetime.datetime.fromtimestamp(int(hour['time'])).strftime('%I:%M %p') ## Convert to GMT 
		hourlyDict['temperature'] = hour['temperature']
		hourlyDict['icon'] = hour['icon']
		hourlyDict['humidity'] = hour['humidity']
		hourlyDict['summary'] = hour['summary']
		hourlyDict['apparentTemperature'] = hour['apparentTemperature']
		hourlyDict['precipProbability'] = hour['precipProbability']
		hourlyDictList.append(hourlyDict)

	current_data = response['currently']
	daily_data = response['daily']['data'][0]

	currentDict = {}
	currentDict['tempMax'] = daily_data['temperatureMax']
	currentDict['tempMin'] = daily_data['temperatureMin']
	currentDict['time'] = datetime.datetime.fromtimestamp(int(current_data['time'])).strftime('%I:%M %p')
	currentDict['temperature'] = current_data['temperature']
	currentDict['icon'] = current_data['icon']
	currentDict['humidity'] = current_data['humidity']
	currentDict['summary'] = current_data['summary']
	currentDict['apparentTemperature'] = current_data['apparentTemperature']
	currentDict['precipProbability'] = current_data['precipProbability']
	currentDict['nearestStormDistance'] = current_data['nearestStormDistance']

	data = tuple([hourlyDictList, currentDict])

	return data








	







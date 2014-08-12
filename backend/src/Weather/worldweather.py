##
## WeatherFetch - WorldWeather.py
## 
## **** THIS FILE IS DESIGNED TO OBTAIN DATA FROM WORLDWEATHER ***  
## 
## Created by: Grant McGovern
## Date: 31 July 2014
## Contact: github.com/g12mcgov 
##
## Purpose: Hits worldweather.com API and recieves data for the rest of the application
##
##
##

import json
import requests

API_KEY = 'a5ffda1f54b0c21545269dcae734661acf2fea72'
BASE_URL = 'http://api.worldweatheronline.com/free/v1/weather.ashx'


def worldWeather(zipcodes):
	response = getWeatherData(zipcodes)

	return response 

def getWeatherData(zipcodes):
	params = {'q':zipcodes, 'num_of_days':'2', 'format':'json', 'key':API_KEY, 'fx':'yes'}
	weather = json.loads(requests.get(url=BASE_URL, params=params).content)

	with open("worldweather.js", "wb") as outfile:
		outfile.write(json.dumps(weather, separators=(',',':'), indent=4))

	return weather
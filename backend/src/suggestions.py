#!/usr/local/bin/python

##
## WeatherFetch - SUGGESTIONS.py.
## 
## **** THIS FILE MAKES APPAREL SUGGESTIONS ***  
## 
## Created by: Grant McGovern
## Date: 31 July 2014
## Contact: github.com/g12mcgov 
##
## Purpose: Using weather data/summaries, attempts to make accurate clothing suggestions.
##
##
##
from random import randint

def suggestion(forecast_io_hourly, current_average, max_average, min_average, previous_pop):
	## Convert to raw pop:
	male = {}
	female = {}

	## Remove parentheses sign previously appended
	pop = float(previous_pop.strip('%'))
	temp = float(max_average)
	
	rain_headers = ["Huh. Looks like it might rain!", "Watchout! Rain inbound!", "Expect some rain today."]
	chilly_headers = ['It might be a little chilly today.', 'Expect some brisk weather.', "It's going to be cool out today."]
	cold_headers = ["It's going to be a cold day today!", "Expect some cold weather today.", "Watchout, it's bitter out there!"]

	## To randomly generate suggestions so they aren't always fed the same content.
	index = randint(0,2)

	## If we are expecting some rain
	if (pop >= 0):
		## Grab headers ##
		male['rain_header'] = rain_headers[index]
		female['rain_header'] = rain_headers[index]
		## If rain, make suggestions.
		male['jacket'] = 'Rain jacket'
		female['jacket'] = 'Rain jacket'
		
		male['umbrella'] = True
		female['umbrella'] = True

	else:
		male['rain_header'] = "No rain today!"
		female['rain_header'] = "No rain today!"

	if (temp >= 65):
		male['top'] = 'Tee shirt or short sleeved shirt'
		female['top'] = 'Dress or short sleeved shirt'
		
		male['bottom'] = 'Shorts or a lightweight pant'
		female['bottom'] = 'Shorts, skirt, or even some light jeans.'
	elif (50 <= temp <= 65):
		male['header'] = chilly_headers[index]
		female['header'] = chilly_headers[index]

		male['top'] = 'Long sleeve shirt, maybe a sweater.'
		female['top'] = 'Long sleeve shirt, perhaps a dress.'
		
		male['bottom'] = 'Pants? Jeans? Your move.'
		female['bottom'] = 'Jeans or pants will do.'
	elif (temp <= 50):
		male['header'] = cold_headers[index]
		female['header'] = cold_headers[index]

		male['top'] = 'Sweater or jacket'
		female['top'] = 'Sweater or jacket'
		
		male['bottom'] = 'Jeans, cords, or some other think pant.'
		female['bottom'] = 'Jeans, leggings, or maybe even cords.'

	## Create Dict to hold suggestions for both genders ##
	suggestionDict = {'male': male, 'female': female}


	return suggestionDict

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

def suggestion(forecast_io_hourly, current_average, max_average, min_average, previous_pop):
	## Convert to raw pop:
	pop = previous_pop
	print pop

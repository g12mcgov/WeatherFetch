##
## WeatherFetch - BODY.py.
## 
## **** THIS FILE CONSTRUCTS THE EMAIL TEMPLATE TO BE SENT ***  
## 
## Created by: Grant McGovern
## Date: 18 August 2014
## Contact: github.com/g12mcgov 
##
## Purpose: This creates the HTML email template using jinja, passing in all necessary variables.
##
##
##

import jinja2

## Not the prettiest. TODO: Change this to a dict structure.
def constructTemplate(forecast_io_current, wunderground_current, hamweather_current, 
			forecast_io_hourly, wunderground_hourly, hamweather_hourly, weather_map, current_average, 
			max_average, min_average, pop):
    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "Users/grantmcgovern/Dropbox/Developer/Projects/WeatherFetch/backend/src/email/email.html"
    template = templateEnv.get_template(TEMPLATE_FILE)

    ## Construct Dict with Weather Info ## 
    templateVars = {}

    ## ForecastIo Dict

    templateVars['forecast_io_current_temp'] = forecast_io_current['temperature']
    templateVars['forecast_io_current_summary'] = forecast_io_current['summary']
    templateVars['forecast_io_current_time'] = forecast_io_current['time']
    templateVars['forecast_io_current_pop'] = forecast_io_current['pop']
    templateVars['forecast_io_current_humidity'] = forecast_io_current['humidity']
    templateVars['forecast_io_current_tempMax'] = forecast_io_current['tempMax']
    templateVars['forecast_io_current_tempMin'] = forecast_io_current['tempMin']
    #templateVars['forecast_io_hourly'] = forecast_io_hourly[2]

    ## Wunderground Dict 
    templateVars['wunderground_current_temp'] = wunderground_current['temperature']
    templateVars['wunderground_current_summary'] = wunderground_current['summary']
    templateVars['wunderground_current_time'] = wunderground_current['time']
    templateVars['wunderground_current_pop'] = wunderground_current['pop']
    templateVars['wunderground_current_humidity'] = wunderground_current['humidity']
    templateVars['wunderground_current_tempMax'] = wunderground_current['tempMax']
    templateVars['wunderground_current_tempMin'] = wunderground_current['tempMin']
    #templateVars['wunderground_hourly'] = wunderground_hourly[0]

    ## HamWeather Dict 
    templateVars['hamweather_current_temp'] = hamweather_current['temperature']
    templateVars['hamweather_current_summary'] = hamweather_current['summary']
    templateVars['hamweather_current_time'] = hamweather_current['time']
    templateVars['hamweather_current_pop'] = hamweather_current['pop']
    templateVars['hamweather_current_humidity'] = hamweather_current['humidity']
    templateVars['hamweather_current_tempMax'] = hamweather_current['tempMax']
    templateVars['hamweather_current_tempMin'] = hamweather_current['tempMin']
    #templateVars['HamWeather_hourly': hamweather_hourly[0]]

    templateVars['current_average'] = current_average
    templateVars['average_pop'] = pop
    templateVars['maxAverage'] = max_average
    templateVars['minAverage'] = min_average

    email_body = template.render(templateVars)

    return email_body 
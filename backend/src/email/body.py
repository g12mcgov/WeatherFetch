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

def constructTemplate(forecast_io_hourly, wunderground_hourly, hamweather_hourly, weather_map, current_average, max_average, min_average, pop):
    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "Users/grantmcgovern/Dropbox/Developer/Projects/WeatherFetch/backend/src/email/email.jinja"
    template = templateEnv.get_template(TEMPLATE_FILE)
    templateVars = {'current_average':current_average}
    email_body = template.render(templateVars)

    return email_body 
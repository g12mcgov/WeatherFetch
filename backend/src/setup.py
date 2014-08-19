#!/usr/local/bin/python

##
## WeatherFetch -SETUP.py.
## 
## **** THIS FILE SETS UP ENVIRONMENT ***  
## 
## Created by: Grant McGovern
## Date: 31 July 2014
## Contact: github.com/g12mcgov 
##
## Purpose: This setups the environment and modules for the application.
##
##
##

from setuptools import setup, find_packages

setup(name = 'WeatherFetch',
	version = '0.1a',
	description = 'A weather service that uses cross-provider data to make incredibly accurate forecasts',
	author = 'Grant McGovern', 
	author_email = 'grantmcgovern.mcgovern@gmail.com',
	install_requires = [
		'multiprocessing',
		'requests',
		'pyzipcode',
		'jinja2',
		'twilio'
	]
)
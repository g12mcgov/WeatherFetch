##
## WeatherFetch - DB.
## 
## **** THIS FILE HANDLES DATABASE WORK ***  
## 
## Created by: Grant McGovern
## Date: 31 July 2014
## Contact: github.com/g12mcgov 
##
## Purpose: Connect to MySQL DB running on Amazon EC2 instance
##
##
##

import MySQLdb
import logging
import time
from datetime import datetime, timedelta

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)

TIME_ZONE = "EDT" # TO CHANGE

def establishDBConnection():
	logger.debug("Establishing Database Connection")

	HOST = "localhost"
	USER = "root"
	PASSWORD = "nantucket"
	DATABASE = "WeatherFetchDB"

	## Keep trying for 10 iterations, if all else fails, we've failed.
	## Break out and log error.
	for attempt in range(10):
		try: 
			connection = MySQLdb.connect(HOST, USER, PASSWORD, DATABASE)
			logger.debug("Successfully established connection.")
			cursor = connection.cursor()
			
			## Returns a cursor the database 
			return cursor 
		
		except MySQLdb.Error as error:
			logging.debug(error)
		# 	raise error

def handleTime(dt=None, roundTo=60):
	if dt == None:
		dt = datetime.utcnow()
	seconds = (dt - dt.min).seconds
	rounding = (seconds + roundTo/2) // roundTo * roundTo
	rounded_time = dt + timedelta(0, rounding - seconds, -dt.microsecond)
	
	## Returns rounded UTC time
	return rounded_time 

def getDBData(cursor):
	## Simply to monitor speed of query. If this gets too big, we
	## may need to find alternative options.
	start_time = time.time() 

	current_time = datetime.utcnow()
	rounded_time = handleTime(current_time, roundTo=60*60).time()

	#USER_QUERY = """ SELECT * FROM WeatherFetchDB.MEMBERS WHERE Time='%s' AND Timezone='%s'""" % (rounded_time, TIME_ZONE)
	USER_QUERY = """ SELECT * FROM WeatherFetchDB.members WHERE Timezone='%s'""" % TIME_ZONE
	cursor.execute(USER_QUERY)
	rows = cursor.fetchall()

	number_of_rows = len(rows)

	if (number_of_rows == 0) or (number_of_rows == None):
		logging.info("No users for time %s.", rounded_time)
		exit() ## Exit entire script -- no need wasting API calls for no users.
	else:
		pass

	end_time = (time.time() - start_time)

	logging.info("Query executed in %f seconds.", end_time)

	return rows


##
## WeatherFetch - WRAPPERS.py.
## 
## **** THIS FILE CONTAINS FUNCTIONAL WRAPPERS ***  
## 
## Created by: Grant McGovern
## Date: 18 August 2014
## Contact: github.com/g12mcgov 
##
## Purpose: Contains wrappers for certain methods.
##
##
##
##

from functools import wraps

def counter(func):
    @wraps(func)
    def tmp(*args, **kwargs):
        tmp.count += 1
        return func(*args, **kwargs)
    tmp.count = 0
    return tmp
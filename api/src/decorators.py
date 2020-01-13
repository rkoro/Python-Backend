#!/usr/bin/python3
import functools
import sys
from datetime import datetime

import src.db as db
import src.ut as ut
from src.arguments import ARGUMENTS
from src.user import GLOBAL_USER

def example(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        value = func(*args, **kwargs)
        return value
    return wrapper_decorator

def timer(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        time = datetime.now().microsecond
        value = func(*args, **kwargs)
        time = datetime.now().microsecond - time
        ut.print_debug("", "pomiar czasu w funkcji {}: {} us = {} ms: ".format(func.__name__, time, time/1000))
        return value
    return wrapper_decorator
	
def timer_error_log(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        time = datetime.now().microsecond
        value = func(*args, **kwargs)
        time = datetime.now().microsecond - time
        marks = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        sys.stderr.write(marks + "pomiar czasu w funkcji {}: {} us = {} ms\n".format(func.__name__, time, time/1000) + marks)
        return value
    return wrapper_decorator

def require_authentication(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        token = ARGUMENTS.getvalue("token")
        if(token):
            if(GLOBAL_USER.login_by_token(token)):
                return func(*args, **kwargs)
            else:
                return ut.response_error("Authentication failed: wrong token")
        else:
            return ut.response_error("This action requires authentication")
    return wrapper_decorator
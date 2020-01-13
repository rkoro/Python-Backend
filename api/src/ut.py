#!/usr/bin/python3
import os
import inspect

def nvl(variable, default = ""):
    if variable is None:
        return default
    return variable

def response_error(message):
    return {
        "error": 1,
        "errorMessage": message,
    }

def response_ok(response = ""):
    return {
        "error": 0,
        "response": response,
    }

def print_debug(data, title = 'DEBUG: '):
    print (title, data, '<br>')

def is_post():
    return os.environ['REQUEST_METHOD'] == 'POST'

def is_get():
    return os.environ['REQUEST_METHOD'] == 'GET'

def get_function(module, function):
    all_functions = inspect.getmembers(module, inspect.isfunction)
    one_function_list = list(filter(lambda x: x[0] == function, all_functions))
    return one_function_list[0][1] if len(one_function_list) == 1 else None
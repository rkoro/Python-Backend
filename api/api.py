#!/usr/bin/python3
print("Content-Type: text/html; charset=UTF-8\n\n")
# print("Content-Type: application/json; charset=UTF-8\n\n")
# import ptvsd

# ptvsd.enable_attach(address=("172.31.4.214", 2345), redirect_output=True)
# ptvsd.wait_for_attach()
import os
import json
import cgitb

cgitb.enable(True)

import src.db as db
import src.ut as ut
from src.arguments import ARGUMENTS
from src.decorators import timer_error_log, require_authentication
from src.user import GLOBAL_USER

BASE_URL = "13.48.189.101"
# python3 -m ptvsd --host 83.11.113.70 --port 12345 --wait -m myproject

db.connect(
    host=BASE_URL,
    # port="5432",
    database="angulardb",
    user="angular",
    password="qwe",
)

(module_name, action_name) = ARGUMENTS.get_path_args_list(2)

if ut.nvl(module_name) == "":
    print(json.dumps(ut.response_error("MODULE NAME IS NOT PROVIED!")))
elif ut.nvl(action_name) == "":
    print(json.dumps(ut.response_error("ACTION NAME IS NOT PROVIDED!")))
else:
    module = None
    try:
        package = __import__("apisrc.{}".format(module_name))
        module = getattr(package, module_name)
    except:
        module = None

    if module:
        prefix = os.environ["REQUEST_METHOD"].lower()
        action_name = "{}_{}".format(prefix, action_name)
        action = ut.get_function(module, action_name)
        if action is not None:
            response = None
            try:
                response = action()
            except:
                response = ut.response_error("UNKNOWN ERROR DURING EXECUTING ACTION")
            print(json.dumps(response))
        else:
            print(json.dumps(ut.response_error("UNKNOWN ACTION")))
    else:
        print(json.dumps(ut.response_error("UNKNOWN MODULE!")))

db.close()

#!/usr/bin/python3
from datetime import datetime
# from arguments import ARGUMENTS
import sys
import ut

def error(error):
    time = datetime.now()
    # (module_name, action_name) = ARGUMENTS.get_path_args_list(2)
    # sys.stderr.write("{} ERROR: {}. Module: {} Action: {}\n".format(time, error, ut.nvl(module_name), ut.nvl(action_name)))
    (module_name, action_name) = ('', '')
    sys.stderr.write("{} ERROR: {}\n".format(time, error))
#!/usr/bin/python3
import cgi
import json
import os
import sys
from datetime import datetime

import src.ut as ut

class PostArguments:
    def __init__(self):
        self.body = sys.stdin.read()
        try:
            self.parsedBody = json.loads(self.body)
        except:
            self.parsedBody = {}
            sys.stderr.write("{} ERROR: error parsing arguments body\n".format(datetime.now()))
    def getvalue(self, v):
        return self.parsedBody[v] if v in self.parsedBody else None

class GetArguments:
    def __init__(self):
        self.arguments = cgi.FieldStorage()
    def getvalue(self, v):
        return self.arguments.getvalue(v)

class ArgumentsClass:
    def __init__(self):
        self.arguments = PostArguments() if ut.is_post() else GetArguments()
        self.path_args = self.get_path_args()

    def get_path_args(self):
        return ut.nvl(os.environ.get("PATH_INFO"), '').split('/')[1:]

    def getvalue(self, v):
        return self.arguments.getvalue(v)

    def get_path_arg(self, index):
        if len(self.path_args) <= index:
            return None
        return self.path_args[index]

    def get_path_args_list(self, length = None):
        if length is None:
            length = len(self.path_args)
        r = []
        for i in range(length):
            r.append(self.get_path_arg(i))
        return r

ARGUMENTS = ArgumentsClass();
#!/usr/bin/python3
import json

import src.ut as ut
from src.arguments import ARGUMENTS
from src.decorators import timer_error_log, require_authentication
from src.user import GLOBAL_USER

def post_login():
    login = ut.nvl(ARGUMENTS.getvalue("login"))
    password = ut.nvl(ARGUMENTS.getvalue("password"))
    if GLOBAL_USER.login(login, password):
        return ut.response_ok({
            "id": GLOBAL_USER.user["id"],
            "login": GLOBAL_USER.user["login"],
            "token": GLOBAL_USER.session["token"]
        })
    else:
        return ut.response_error("User Not Found")

@require_authentication
def post_logout():
    GLOBAL_USER.logout()
    return ut.response_ok();
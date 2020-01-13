#!/usr/bin/python3
import json

import src.db as db
import src.ut as ut
from src.arguments import ARGUMENTS
from src.decorators import timer_error_log, require_authentication
from src.user import GLOBAL_USER

# @timer_error_log
# @require_authentication
def get_get_items():
    return db.fetch('test')

def post_add_item():
    item = ARGUMENTS.getvalue("item")
    if item:
        response = None
        try:
            item = json.loads(item)
            response = ut.response_ok({
                "id": db.insert('test', item)
            })
        except:
            response = ut.response_error("ERROR PARSING DATA!")
        return response
    else:
        return ut.response_error("NO ITEM PROVIDED!")

def post_delete_item():
    id = ut.nvl(ARGUMENTS.getvalue("id"), "-1")
    rows_deleted = db.delete('test', "id = %s", [id])
    return ut.response_ok({
        "rows_deleted": rows_deleted
    })
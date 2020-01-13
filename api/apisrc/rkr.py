#!/usr/bin/python3
import json

import src.db as db
import src.ut as ut
import datetime
import random
from src.arguments import ARGUMENTS
from src.decorators import timer_error_log, require_authentication
from src.user import GLOBAL_USER


def get_getItems():
    items = db.fetch("liczby")
    return list(
        map(
            lambda x: {
                "id": x["id"],
                "liczba_uz": x["liczba_uz"],
                "liczba_gen": x["liczba_gen"],
                "data_wpisu": str(x["data_wpisu"]),
            },
            items,
        )
    )


def post_addItem():
    liczba_uz = ARGUMENTS.getvalue("liczba_uz")
    liczba_gen = random.randrange(0, 10000)
    data = datetime.date.today().strftime("%Y-%m-%d")
    id = db.insert(
        "liczby",
        {"liczba_uz": liczba_uz, "liczba_gen": liczba_gen, "data_wpisu": data,},
    )
    return ut.response_ok({"nowy_id": id})


def post_deleteItem():
    raw_id = ARGUMENTS.getvalue("id")
    id = ut.nvl(raw_id, "-1")  # ARGUMENTS.getvalue("id")
    rows_deleted = db.delete("liczby", "id = %s", [id])
    return ut.response_ok({"rows_deleted": rows_deleted, "id": id, "raw_id": raw_id})


# @timer_error_log
# @require_authentication
# def get_get_items():
#     return db.fetch("test")


# def post_add_item():
#     item = ARGUMENTS.getvalue("item")
#     if item:
#         response = None
#         try:
#             item = json.loads(item)
#             response = ut.response_ok({"id": db.insert("test", item)})
#         except:
#             response = ut.response_error("ERROR PARSING DATA!")
#         return response
#     else:
#         return ut.response_error("NO ITEM PROVIDED!")


# def post_delete_item():
#     id = ut.nvl(ARGUMENTS.getvalue("id"), "-1")
#     rows_deleted = db.delete("test", "id = %s", [id])
#     return ut.response_ok({"rows_deleted": rows_deleted})


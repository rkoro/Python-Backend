#!/usr/bin/python3
import hashlib
from datetime import datetime

import src.db as db

class User:
    user = None
    session = None

    def login(self, login, password):
        user = db.fetch_one('users',
            fields='id, login, password, email, created',
            filter="login=%s AND password=%s",
            args=[login, password]
        )
        if user is not None:
            self.user = user
            time = datetime.now().microsecond
            random = 17
            token = hashlib.md5("{}_{}_{}".format(self.user["login"], time, random).encode('utf-8')).hexdigest()
            db.insert('users_sessions', {
                "token": token,
                "userid": self.user["id"]
            })
            self.session = db.fetch_one('users_sessions',
                filter="token=%s",
                args=[token]
            )
            return True
        return False
    
    def login_by_token(self, token):
        session = db.fetch_one('users_sessions',
            filter="token=%s",
            args=[token]
        )
        if session is not None:
            self.session = session
            self.user = db.fetch_one('users',
                filter="id=%s",
                args=[self.session["userid"]]
            )
            return True
        return False

    def isLoggedIn(self):
        return self.user is not None

    def logout(self):
        if self.session["id"]:
            db.delete('users_sessions', "id=%s", args=[self.session["id"]])
            self.session = None
            self.user = None

GLOBAL_USER = User()
from pony.orm import Required

from app import db


class User(db.Entity):
    user_key = Required(str)
    nickname = Required(str)

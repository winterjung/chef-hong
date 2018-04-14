from datetime import datetime

from app import db


class ModelMixin:
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


class User(ModelMixin, db.Model):
    user_key = db.Column(db.String, nullable=False, unique=True)
    nickname = db.Column(db.String, nullable=True)

    def __init__(self, user_key, nickname=None):
        self.user_key = user_key
        self.nickname = nickname

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.user_key)

from sqlalchemy import Column, String, Integer, Boolean

from bot import db


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    fb_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    is_authorized = Column(Boolean)

    def __init__(self, fb_id, first_name, last_name, gender, is_authorized=False):
        self.fb_id = fb_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.is_authorized = is_authorized

    def set_authorized(self, value):
        self.is_authorized = value

    def __repr__(self):
        return '<id {} - {} {} Gender: {}>'.format(self.fb_id, self.first_name, self.last_name, self.gender)

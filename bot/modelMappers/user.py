import logging

from sqlalchemy import and_
from bot.database import Database
from bot.models.user import User


class UserMapper(object):

    # Create
    def create_user(self, fb_id, first_name, last_name, gender):
        u = User(fb_id, first_name, last_name, gender)
        Database.add_to_db(u)
        logging.debug("Adding user {} - {} {} to database".format(fb_id,
                                                                  first_name,
                                                                  last_name))
        return u

    # Read
    def get_user_by_fb_id(self, fb_id):
        u = User.query.filter(User.fb_id == fb_id).first()
        if u:
            return u
        else:
            raise ValueError("User not found", fb_id)

    def get_all_users(self):
        users = User.query.all()
        return users

    def get_all_males(self):
        users = User.query.filter(User.gender == "male")
        return users

    def get_all_females(self):
        users = User.query.filter(User.gender == "female")
        return users

    def get_other_genders(self):
        users = User.query.filter(and_(User.gender != "male",
                                       User.gender != "female"))
        return users

    # Update
    def update_user_authorization(self, fb_id, value):
        u = User.query.filter(User.fb_id == fb_id).first()
        if u:
            u.set_authorized(True)
            Database.commit_db()
            logging.debug("Updating {} - {} {} to database".format(fb_id,
                                                                   u.first_name,
                                                                   u.last_name))
            return u
        else:
            raise ValueError("User not found", fb_id)

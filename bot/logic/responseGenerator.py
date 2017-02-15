import random

from bot.constants.messages import *
from bot.logic.facebook import Facebook


class ResponseGenerator(object):

    def __init__(self):
        self.fb = Facebook()

    def choose_response(self, lst):
        return random.choice(lst)

    def generic_response(self, user, lst):
        response = self.choose_response(lst)
        self.fb.send_message_text(user.fb_id, response)

    def laugh(self, user):
        self.generic_response(user, LAUGH)

    def thank(self, user):
        self.generic_response(user, THANK)

    def greeting(self, user):
        self.generic_response(user, GREETING)

    def farewell(self, user):
        self.generic_response(user, FAREWELL)

    def command_not_found(self, user):
        self.generic_response(user, COMMAND_NOT_FOUND)

    def gombal(self, user):
        self.fb.send_message_bubble(user.fb_id)
        word = self.choose_response(GOMBALAN)
        self.fb.send_message_gombal(user.fb_id, word)

    def welcome_message(self, user):
        self.fb.send_message_bubble(user.fb_id)
        self.fb.send_message_text(
            user.fb_id, WELCOME_MESSAGE.format(user.first_name))

    def send_like(self, user):
        self.fb.send_message_text(
            user.fb_id, self.choose_response(LIKE_MESSAGE).format(user.first_name))

    def send_authorization(self, user):
        self.fb.send_message_authorization(user.fb_id)

    def send_match(self, user, u):
        self.fb.send_message_picture(user, u)

    def match_not_found(self, user):
        self.fb.send_message_text(
            user.fb_id, NOT_FOUND.format(user.first_name))

    def send_match_again(self, user):
        self.generic_response(user, REQUEST_AGAIN)

    def stop_send_match(self, user):
        self.fb.send_message_text(
            user.fb_id, self.choose_response(REQUEST_STOP).format(user.first_name))

    def get_user_data(self, fb_id):
        return self.fb.get_user_data(fb_id)

    def not_authorized(self, user):
        self.generic_response(user, NOT_AUTHORIZED)

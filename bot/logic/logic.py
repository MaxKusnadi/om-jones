import logging
import json
import os
import requests
import random

from bot.constants.messages import *
from bot.logic.facebook import Facebook
from bot.modelMappers.user import UserMapper


class Logic(object):

    def __init__(self):
        self.user = UserMapper()
        self.fb = Facebook()

    def get_all_users(self):
        u = self.user.get_all_users()
        return u

    def parse_messaging_event(self, messaging_event):
        sender_id = messaging_event["sender"]["id"]
        recipient_id = messaging_event["recipient"]["id"]
        user = self.find_user(sender_id)
        if messaging_event.get("message"):  # someone sent us a message
            self.parse_message(user, messaging_event)

        if messaging_event.get("delivery"):  # delivery confirmation
            pass

        if messaging_event.get("optin"):  # optin confirmation
            pass

        # user clicked/tapped "postback" button in earlier message
        if messaging_event.get("postback"):
            self.fb.send_message_bubble(sender_id)
            self.fb.send_message_text(
                sender_id, WELCOME_MESSAGE.format(user.first_name))

    def parse_message(self, user, messaging_event):
        self.fb.send_message_bubble(user.fb_id)
        if "quick_reply" in messaging_event["message"].keys():
            self.process_quick_reply(user.fb_id, messaging_event[
                                     "message"]["quick_reply"]["payload"])
        else:
            try:
                message_text = messaging_event["message"]["text"]
            except KeyError:
                self.fb.send_message_text(
                    user.fb_id, LIKE_MESSAGE.format(user.first_name))
            else:
                if message_text.lower() == "anti jones":
                    self.fb.send_message_text(user.fb_id, "Bentar ya bro")
                else:
                    self.give_gombalan(user)

    def give_gombalan(self, user):
        self.fb.send_message_text(user.fb_id, GOMBALAN_MESSAGE)
        self.fb.send_message_bubble(user.fb_id)
        word = random.choice(GOMBALAN)
        self.fb.send_message_text(user.fb_id, word)
        self.fb.send_message_text(user.fb_id, "Pake tuh mblo")

    def process_quick_reply(self, sender_id, payload):
        pass

    def find_user(self, fb_id):
        try:
            u = self.user.get_user_by_fb_id(fb_id)
        except ValueError as err:
            logging.error(err)
            first_name, last_name, gender, pic = self.fb.get_user_data(fb_id)
            u = self.user.create_user(fb_id, first_name, last_name, gender)
        return u

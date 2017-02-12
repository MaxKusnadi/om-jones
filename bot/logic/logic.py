import logging
import json
import os
import requests
import random

from bot.constants.messages import *
from bot.logic.facebook import Facebook
from bot.logic.processor import Processor
from bot.modelMappers.user import UserMapper


class Logic(object):

    def __init__(self):
        self.user = UserMapper()
        self.fb = Facebook()
        self.processor = Processor()

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
            self.process_quick_reply(user, messaging_event[
                                     "message"]["quick_reply"]["payload"])
        else:
            try:
                message_text = messaging_event["message"]["text"]
            except KeyError:
                self.fb.send_message_text(
                    user.fb_id, LIKE_MESSAGE.format(user.first_name))
            else:
                if message_text.lower() == "anti jones":
                    self.find_match(user)
                else:
                    self.give_gombalan(user)

    def find_match(self, user):
        gender = user.gender

        if gender == "male":
            u = self.generate_match(self.processor.get_match_for_male)
        elif gender == "female":
            u = self.generate_match(self.processor.get_match_for_female)
        else:
            u = self.generate_match(self.processor.get_match_for_others)

        if u:
            self.fb.send_message_picture(user, u)
        else:
            self.fb.send_message_text(
                user.fb_id, NOT_FOUND.format(user.first_name))

    def generate_match(self, fn):
        try:
            u = fn()
        except IndexError as err:
            u = None
        return u

    def give_gombalan(self, user):
        self.fb.send_message_text(user.fb_id, GOMBALAN_MESSAGE)
        self.fb.send_message_bubble(user.fb_id)
        word = random.choice(GOMBALAN)
        self.fb.send_message_text(user.fb_id, word)
        self.fb.send_message_text(
            user.fb_id, "Kalo mau Om cariin jomblo laen, bilang 'anti jones' yak")

    def process_quick_reply(self, user, payload):
        if payload == "Yes":
            self.fb.send_message_text(user.fb_id, REQUEST_AGAIN)
            self.find_match(user)
        else:
            self.fb.send_message_text(
                user.fb_id, REQUEST_STOP.format(user.first_name))

    def find_user(self, fb_id):
        try:
            u = self.user.get_user_by_fb_id(fb_id)
        except ValueError as err:
            logging.error(err)
            first_name, last_name, gender, pic = self.fb.get_user_data(fb_id)
            u = self.user.create_user(fb_id, first_name, last_name, gender)
        return u

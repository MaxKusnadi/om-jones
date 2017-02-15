import logging
import json
import os
import requests
import random

from bot.constants.messages import *
from bot.logic.facebook import Facebook
from bot.logic.processor import Processor
from bot.logic.responseGenerator import ResponseGenerator
from bot.modelMappers.user import UserMapper
from bot.witai import client


class Logic(object):

    def __init__(self):
        self.user = UserMapper()
        self.processor = Processor()
        self.wit = client
        self.response = ResponseGenerator()

    def get_all_users(self):
        u = self.user.get_all_users()
        return u

    def parse_messaging_event(self, messaging_event):
        sender_id = messaging_event["sender"]["id"]
        recipient_id = messaging_event["recipient"]["id"]
        user = self.find_user(sender_id)
        if messaging_event.get("message"):  # someone sent us a message
            self.parse_message(user, messaging_event)

        # user clicked/tapped "postback" button in earlier message
        if messaging_event.get("postback"):
            self.response.welcome_message(user)

    def parse_message(self, user, messaging_event):
        if "quick_reply" in messaging_event["message"].keys():
            self.process_quick_reply(user, messaging_event[
                                     "message"]["quick_reply"]["payload"])
        else:
            try:
                message_text = messaging_event["message"]["text"]
            except KeyError:
                self.response.send_like(user)
            else:
                if message_text.lower() == "anti jones":
                    self.check_user_authorization(user)
                else:
                    fn = self.process_with_wit(message_text)
                    fn(user)

    def check_user_authorization(self, user):
        if user.is_authorized:
            self.find_match(user)
        else:
            self.response.send_authorization(user)

    def find_match(self, user):
        gender = user.gender

        if gender == "male":
            u = self.generate_match(self.processor.get_match_for_male)
        elif gender == "female":
            u = self.generate_match(self.processor.get_match_for_female)
        else:
            u = self.generate_match(self.processor.get_match_for_others)

        if u:
            self.response.send_match(user, u)
        else:
            self.response.match_not_found(user)

    def generate_match(self, fn):
        try:
            u = fn()
        except IndexError as err:
            u = None
        return u

    def process_quick_reply(self, user, payload):
        if payload == "Yes":
            self.response.send_match_again(user)
            self.find_match(user)
        elif payload == "No":
            self.response.stop_send_match(user)
        elif payload == "Authorized":
            self.user.update_user_authorization(user.fb_id, True)
            self.response.send_match_again(user)
            self.find_match(user)
        elif payload == "gombal_lagi":
            self.response.gombal(user)
        elif payload == "gombal_stop":
            self.response.farewell(user)
        else:
            self.response.not_authorized(user)

    def find_user(self, fb_id):
        try:
            u = self.user.get_user_by_fb_id(fb_id)
        except ValueError as err:
            logging.error(err)
            first_name, last_name, gender, pic = self.response.get_user_data(
                fb_id)
            u = self.user.create_user(fb_id, first_name, last_name, gender)
        return u

    def process_with_wit(self, message):
        resp = self.wit.message(message)
        entity, value = self.parse_wit(resp)

        if entity == 'laugh':
            return self.response.laugh
        elif entity == 'thank':
            return self.response.thank
        elif entity == 'gombal':
            return self.response.gombal
        elif entity == 'intent':
            if value == "greeting":
                return self.response.greeting
            else:
                return self.response.farewell
        else:
            return self.response.command_not_found

    def parse_wit(self, resp):
        resp_entity = resp['entities']
        entities = ['thank', 'intent', 'gombal', 'laugh']
        best_entity = None
        best_accuracy = 0
        best_value = None
        for en in entities:
            if en in resp_entity:
                accuracy = resp_entity[en][0]['confidence']
                if accuracy >= 0.8 and accuracy >= best_accuracy:
                    best_entity = en
                    best_accuracy = accuracy
                    best_value = resp_entity[en][0]['value']
        return (best_entity, best_value)

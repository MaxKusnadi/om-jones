import logging
import json
import os
import requests


class Facebook(object):

    def __init__(self):
        self.PARAMS = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }
        self.HEADERS = {
            "Content-Type": "application/json"
        }
        self.LINK = "https://graph.facebook.com/v2.6/me/messages"

    def get_user_data(self, fb_id):
        logging.info("getting info of {recipient}".format(recipient=fb_id))
        link = "https://graph.facebook.com/v2.6/" + \
            fb_id + "?fields=first_name,last_name,gender,profile_pic"
        r = requests.get(link, params=self.PARAMS, headers=self.HEADERS)
        if r.status_code != 200:
            logging.info(r.status_code)
            logging.info(r.text)
        result = r.json()
        return (result['first_name'], result['last_name'], result['gender'], result['profile_pic'])

    def send_message_bubble(self, fb_id):
        logging.info("sending message bubble to {recipient}".format(
            recipient=fb_id))

        data = json.dumps({
            "recipient": {
                "id": fb_id
            },
            "sender_action": "typing_on"
        })
        r = requests.post(self.LINK, params=self.PARAMS,
                          headers=self.HEADERS, data=data)
        if r.status_code != 200:
            logging.info(r.status_code)
            logging.info(r.text)

    def send_message_text(self, recipient_id, message_text):
        logging.info("sending message to {recipient}: {text}".format(
            recipient=recipient_id, text=message_text))

        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })
        r = requests.post(self.LINK, params=self.PARAMS,
                          headers=self.HEADERS, data=data)
        if r.status_code != 200:
            logging.info(r.status_code)
            logging.info(r.text)

    def start_order(self, recipient_id):
        logging.info("starting order for {recipient}".format(
            recipient=recipient_id))

        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": "Which flower do you want?",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Packet A",
                        "payload": "Packet A",
                        "image_url": "https://cdn.pixabay.com/photo/2013/06/23/19/47/rose-140853_960_720.jpg"
                    },
                    {
                        "content_type": "text",
                        "title": "Packet B",
                        "payload": "Packet B",
                        "image_url": "https://cdn.pixabay.com/photo/2013/05/26/12/14/rose-113735_960_720.jpg"
                    }
                ]
            }
        })
        r = requests.post(self.LINK, params=self.PARAMS,
                          headers=self.HEADERS, data=data)
        if r.status_code != 200:
            logging.info(r.status_code)
            logging.info(r.text)

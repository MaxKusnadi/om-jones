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

    def send_message_gombal(self, recipient_id, message_text):
        logging.info("sending message to {recipient}: {text}".format(
            recipient=recipient_id, text=message_text))

        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text,
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Gombal lagi Om",
                        "payload": "gombal_lagi",
                    },
                    {
                        "content_type": "text",
                        "title": "Udahan ah cape",
                        "payload": "gombal_stop",
                    }
                ]
            }
        })
        r = requests.post(self.LINK, params=self.PARAMS,
                          headers=self.HEADERS, data=data)
        if r.status_code != 200:
            logging.info(r.status_code)
            logging.info(r.text)

    def send_message_picture(self, origin, target):
        first_name, last_name, gender, pic = self.get_user_data(target.fb_id)
        self.send_message_text(origin.fb_id, "Nih buat lu mblo, {first_name}".format(
            first_name=first_name))

        logging.info("sending match for {recipient}".format(
            recipient=origin.fb_id))

        data = json.dumps({
            "recipient": {
                "id": origin.fb_id
            },
            "message": {
                "attachment": {
                    "type": "image",
                    "payload": {
                        "url": pic
                    }
                },
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Lagi dong Om",
                        "payload": "Yes",
                    },
                    {
                        "content_type": "text",
                        "title": "Udahan ah",
                        "payload": "No",
                    }
                ]
            }
        })
        r = requests.post(self.LINK, params=self.PARAMS,
                          headers=self.HEADERS, data=data)
        if r.status_code != 200:
            logging.info(r.status_code)
            logging.info(r.text)

    def send_message_authorization(self, recipient_id):
        logging.info("sending authorization message to {recipient}".format(
            recipient=recipient_id))

        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": "Untuk lanjut, Om perlu store nama dan foto kamu. Data kamu aman kok sama Om. Janji deh. Kamu setuju?",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Ok deh Om. Tancaap",
                        "payload": "Authorized",
                    },
                    {
                        "content_type": "text",
                        "title": "Yah aku masih takut nih",
                        "payload": "Not authorized",
                    }
                ]
            }
        })
        r = requests.post(self.LINK, params=self.PARAMS,
                          headers=self.HEADERS, data=data)
        if r.status_code != 200:
            logging.info(r.status_code)
            logging.info(r.text)

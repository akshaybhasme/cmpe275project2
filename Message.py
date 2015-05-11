__author__ = 'akshaybhasme'

import json


class Message:

    def __init__(self, msg_type, payload):
        self.msg_type = msg_type
        self.payload = payload

    def set_msg_type(self, msg_type):
        self.msg_type = msg_type

    def set_msg_payload(self, payload):
        self.payload = payload

    def get_message_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

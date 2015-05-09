__author__ = 'akshaybhasme'

class Message:

    def __init__(self, type, payload):
        self.type = type
        self.payload = payload

    def getMessageJSON(self):
        return "{\"type\" : "+self.type+", \"message\": \""+self.payload+"\"}"

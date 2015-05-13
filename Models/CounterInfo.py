__author__ = 'apurvapawar'

class CounterInfo:

    def __init__(self):
        self.name = ""
        self.ip = ""
        self.port = ""
        self.busy = False

    def get_name(self):
        return self.name

    def set_name(self, n):
        self.name = n

    def get_name(self):
        return self.ip

    def set_ip(self, i):
        self.ip = i

    def get_port(self):
        return self.port

    def set_port(self, p):
        self.port = p

    def is_busy(self):
        return self.busy

    def set_status(self, b):
        self.busy = b
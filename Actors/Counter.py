__author__ = 'priya'
import state
import Attendant


class Counter:
    def __init__(self, attendant, state):
        self.Attendant = attendant
        self.State = state

    def has_attendant(self):
        if self.Attendant is None:
            return False
        else:
            return True

    def add_attendant(self, attendant):
        self.Attendant = attendant

    def remove_attendant(self):
        self.Attendant = None
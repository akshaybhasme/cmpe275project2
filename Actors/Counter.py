__author__ = 'priya'

class Counter:
    def __init__(self, Attendant, State):
        self.Attendant = Attendant
        self.State = State

    def hasAttendant(self):
        if self.Attendant is None:
            return False
        else:
            return True

    def addAttendant(self, Attendant):
        self.Attendant = Attendant

    def removeAttendant(self):
        self.Attendant = None
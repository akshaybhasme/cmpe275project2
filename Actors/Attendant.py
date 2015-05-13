import Models.Item as Item


class Attendant:
    def __init__(self):
        self.alcoholic = False
        self.total = 0
        self.alcohol_cost = 0
        self.state = 'Idle'

    def process_item_list(self, items):
        if self.state == 'Idle':
            self.state = 'Busy'
            for item in items:
                if item.is_alcoholic():
                    self.alcohol_cost += item.get_value()
                    self.alcoholic = True
                    # The program needs to wait here to get the ID instead of processing the items, or does it?
                    # Maybe the attendant purposely keeps the liquor item for the end
                self.total = self.total + item.get_value()
            # print("Items processed. Your total is: ", self.total)
            return self.alcoholic

    def remove_alcoholic(self):
        self.total -= self.alcohol_cost
        return "Alcoholic items worth ", self.alcohol_cost, "have been removed. "

    def get_total(self):
        reply = "Your total today is: $", self.total
        return reply

    def process_card(self):
        # need to check for failure and cash back
        reply = "PAYMENT SUCCESSFUL: Amount deducted from Card :$", self.total
        return reply

    def process_cash(self, cash):
        self.total -= cash
        reply = None
        if self.total > 0:
            reply = "Sorry, but your short by:$ ", self.total
        elif self.total < 0:
            reply = "Thank you. Here's you change: $", abs(self.total), "Have a nice day. :)"
            self.total = 0
        else:
            reply = "Thank you. Your payment is processed. Have a nice day. :)"
        return reply

    def become_idle(self):
        self.state = 'Idle'
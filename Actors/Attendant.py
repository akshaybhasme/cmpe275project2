import Models.Item as Item


class Attendant:
    def __init__(self):
        self.alcoholic = False
        self.total = 0
        self.alcohol_cost = 0
        self.state = 'Idle'

    def process_item_list(self, items):
        # item needs to behave like Models.Item object. Will this work?
        if self.state == 'Idle':
            self.state = 'Busy'
            for item in items:
                if item.is_alcoholic():
                    self.alcohol_cost = item.get_value()
                    if self.alcoholic:
                        print("Another Alcoholic item found")
                    else:
                        print("Alcoholic item found. ID card is required to process item")
                        self.alcoholic = True
                    # The program needs to wait here to get the ID instead of processing the items, or does it?
                    # Maybe the attendant purposely keeps the liquor item for the end
                self.total = self.total + item.get_value()
            print("Items processed. Your total is: ", self.total)
            return self.alcoholic
        else:
            print("Attendant Busy. Please wait for your turn")

    def remove_alcoholic(self):
        self.total -= self.alcohol_cost
        print("Alcoholic items worth ", self.alcohol_cost, " removed")

    def process_card(self):
        print("PAYMENT SUCCESS: Amount deducted from Card :$", self.total)
        return True

    def process_cash(self, cash):
        self.total -= cash
        if self.total > 0:
            print("PAYMENT UNSUCCESSFUL: Insufficient funds")
            return False
        elif self.total < 0:
            print("PAYMENT SUCCESS: Cash collected")
            print("Change Returned", abs(self.total))
            self.total = 0
        else:
            print("PAYMENT SUCCESS: Cash collected")
        return True

    def become_idle(self):
        self.state = 'Idle'
__author__ = 'priya'
import time
from random import randint


class Attendant:
    def __init__(self, queue):
        self.Queue = queue
        self.Customer = self.Queue.get()

    def process_item_list(self):
        for item in self.Customer.items:
            if item.isAlcoholic:
                self.process_alcohol()
            else:
                self.process_nonalcohol(item)

    def process_nonalcohol(self, item):
        time.sleep(randint(3,5))
        print("Processing item: ", item)

    def payment(self):
        if self.Customer.hasDebitOrCreditCard:
            time.sleep(randint(3,5))
            print("PAYMENT SUCCESS: Amount deducted from Card")
        else:
            time.sleep(randint(5,8))
            print("PAYMENT SUCCESS: Cash collected")

    def process_alcohol(self):
        if self.Customer.hasAgeProof:
            time.sleep(randint(10,15))
            print("Processing alcoholic item")
        else:
            print("Customer: ", self.Customer,"does not have an ID card")
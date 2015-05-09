from random import randint

from Models import Item

MAX_ITEMS = 10
CARD_PROBABILITY = 50
LEGAL_AGE = 21
AGE_PROOF_PROBABILITY = 80
MAX_CASH_IN_HAND = 500


class Customer:
    def __init__(self):
        self.isAdult = False
        self.hasAgeProof = False
        self.hasDebitOrCreditCard = False
        self.cashOnHand = 0
        self.items = []
        self.generate_customer()

    def generate_items(self):
        for x in range(0, MAX_ITEMS):
            item = Item()
            self.items.append(item)

    def generate_customer(self):
        if randint(0, 100) > CARD_PROBABILITY:
            self.hasDebitOrCreditCard = True

        if randint(0, 80) > LEGAL_AGE:
            self.isAdult = True
            if randint(0, 100) > 100 - AGE_PROOF_PROBABILITY:
                self.hasAgeProof = True

        self.cashOnHand = randint(0, MAX_CASH_IN_HAND)
        self.generate_items()
__author__ = 'apurvapawar'

from random import randint

from Models import Item
from Config import info


MAX_ITEMS = info.customer['MAX_ITEMS']
CARD_PROBABILITY = info.customer['CARD_PROBABILITY']
LEGAL_AGE = info.customer['LEGAL_AGE']
AGE_PROOF_PROBABILITY = info.customer['AGE_PROOF_PROBABILITY']
MAX_CASH_IN_HAND = info.customer['MAX_CASH_IN_HAND']


class Customer:
    def __init__(self):
        self.isAdult = False
        self.hasAgeProof = False
        self.hasDebitOrCreditCard = False
        self.cashOnHand = 0
        self.items = []
        self.timestamp = None
        self.generate_customer()

    def generate_items(self):
        total = randint(1, MAX_ITEMS)
        for x in range(0, total):
            item = Item.Item()
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

    def is_adult(self):
        return self.isAdult

    def has_age_proof(self):
        return self.hasAgeProof

    def has_debit_or_credit_card(self):
        return self.hasDebitOrCreditCard

    def get_cash_on_hand(self):
        return self.cashOnHand

    def get_items(self):
        return self.items

    def get_timestamp(self):
        return self.timestamp

    def set_adult(self, is_adult):
        self.isAdult = is_adult
        
    def set_has_age_proof(self, has_age_proof):
        self.hasAgeProof = has_age_proof

    def set_debit_or_credit(self, debit_or_credit_card):
        self.hasDebitOrCreditCard = debit_or_credit_card

    def set_cash_in_hand(self, cash_in_hand):
        self.cashOnHand = cash_in_hand

    def set_items(self, items):
        self.items = items

    def set_timestamp(self, t):
        self.timestamp = t

    def object_decoder(self, obj):
        self.isAdult = obj['isAdult']
        self.hasAgeProof = obj['hasAgeProof']
        self.hasDebitOrCreditCard = obj['hasDebitOrCreditCard']
        self.cashOnHand = obj['cashOnHand']
        for item_json in obj['items']:
            item = Item.Item()
            item.decode_from_json(item_json)
            self.items.append(item)
__author__ = 'apurvapawar'

from random import randint

MAX_ITEM_VALUE = 50
ITEM_ALCOHOL_PROBABILITY = 10


class Item:
    def __init__(self):
        self.name = ""
        self.value = 0
        self.isAlcoholic = False
        self.generate_item()

    def generate_item(self):
        self.name = "IN " + str(randint(1, 5000))
        self.value = randint(1, MAX_ITEM_VALUE)

        if randint(0, 100) < ITEM_ALCOHOL_PROBABILITY:
            self.isAlcoholic = True

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def is_alcoholic(self):
        return self.isAlcoholic
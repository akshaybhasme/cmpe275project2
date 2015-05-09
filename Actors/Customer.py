from Models import Item


class Customer:
    def __init__(self):
        self.hasAgeProof = False
        self.hasDebitOrCreditCard = False
        self.items = []
        self.generate_items()

    def generate_items(self):
        for x in range(0, 9):
            item = Item()
            self.items.append(item)
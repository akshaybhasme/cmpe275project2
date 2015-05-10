__author__ = 'jatin'

import Queue
import Customer


class CustomerQueue:

    def __init__(self):
        self.q = Queue.Queue()

    def add_customer(self, customer):
        self.q.put(customer)

    def get_customer(self):
        customer = self.q.get()
        return customer


def main():
    q = CustomerQueue()
    customer = Customer.Customer()
    q.add_customer(customer)
    customer = q.get_customer()
    items = customer.get_items()
    print len(items)
    for item in items:
        print("Name: " + item.get_name() +
              " Value: $" + str(item.get_value()) +
              " isAlcoholic?: " + str(item.is_alcoholic()))


if __name__ == '__main__':
    main()
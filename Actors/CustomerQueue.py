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
    print("hello")
    q = CustomerQueue()
    customer = Customer.Customer()
    q.add_customer(customer)
    customer = q.get_customer()
    print(customer.cashOnHand)


if __name__ == '__main__':
    main()
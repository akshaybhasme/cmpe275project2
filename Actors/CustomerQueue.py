__author__ = 'jatin'

import Queue
import Customer

class CustomerQueue:


    def __init__(self):
        self.q = Queue.Queue()

    def addCustomer(self, customer):
        self.q.put(customer)

    def getCustomer(self):
        cust = Customer.Customer()
        cust = self.q.get()
        return cust




def main():
    print("hello")
    q = CustomerQueue()
    cust = Customer.Customer()
    q.addCustomer(cust)
    cust =  q.getCustomer()
    print(cust)











if __name__ == '__main__':
    main()
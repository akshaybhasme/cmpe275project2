__author__ = 'akshaybhasme'

from twisted.internet import protocol, reactor, endpoints
from Actors.CustomerQueue import CustomerQueue
from Actors.Customer import Customer
import json
from Message import Message


class CustomerQueueServer(protocol.Protocol):

    def __init__(self, cqFactory):
        self.customerQueueFactory = cqFactory
        pass

    def dataReceived(self, data):
        print data
        try:
            message = json.loads(data)

            if message['msg_type'] == 'addcustomer':
                print "Adding customer"
                customer = Customer()
                customer.object_decoder(message['payload'])
                self.customerQueueFactory.add_to_queue(customer)
                print "Customer added"

            elif message['msg_type'] == 'nextcustomer':
                print "Sending customer"
                msg = Message('customer', self.customerQueueFactory.get_from_queue())
                msg_json = json.dumps(msg, default=lambda o: o.__dict__)
                print msg_json
                self.transport.write(msg_json)
                print "Customer sent"
        except Exception as e:
            print e.message
            self.transport.write("Dude, you screwed up! :(")


class CustomerQueueFactory(protocol.Factory):
    def __init__(self):
        self.q = CustomerQueue()
        pass

    def add_to_queue(self, customer):
        self.q.add_customer(customer)

    def get_from_queue(self):
        return self.q.get_customer()

    def buildProtocol(self, addr):
        print "Got connection"
        return CustomerQueueServer(self)


def main():
    customerQueueFactory = CustomerQueueFactory()
    endpoints.serverFromString(reactor, "tcp:1234").listen(customerQueueFactory)
    reactor.run()


if __name__ == '__main__':
    main()
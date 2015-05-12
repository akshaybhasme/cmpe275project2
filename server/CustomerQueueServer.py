__author__ = 'akshaybhasme'

from twisted.internet import protocol, reactor, endpoints
from Actors.CustomerQueue import CustomerQueue
from Actors.Customer import Customer
import json
from Message import Message


class CustomerQueueServer(protocol.Protocol):

    def __init__(self):
        self.q = CustomerQueue()

    def dataReceived(self, data):
        print data
        try:
            message = json.loads(data)

            if message['type'] == 'addcustomer':
                customer = Customer()
                self.q.add_customer(customer)
                print "Customer added"

            elif message['type'] == 'nextcustomer':
                msg = Message('customer', self.q.get_customer())
                self.transport.write(json.dumps(msg, default=lambda o: o.__dict__))
                print "Customer sent"

        except:
            # print exception here if you want a debug statement
            pass


class CustomerQueueFactory(protocol.Factory):
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return CustomerQueueServer()

endpoints.serverFromString(reactor, "tcp:1234").listen(CustomerQueueFactory())
reactor.run()

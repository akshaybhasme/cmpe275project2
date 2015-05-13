__author__ = 'akshaybhasme'

from twisted.internet import protocol, reactor, endpoints
import json
import copy

from Actors.CustomerQueue import CustomerQueue
from Actors.Customer import Customer
from Message import Message
from Config import server


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
                if self.customerQueueFactory.has_customer():
                    msg = Message('customer', self.customerQueueFactory.get_from_queue())
                else:
                    msg = Message('no_customer', "")

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

    def has_customer(self):
        return self.q.has_customer()

    def buildProtocol(self, addr):
        print "Got connection from "+str(addr)
        return CustomerQueueServer(self)


class CounterHouse:

    def __init__(self):
        self.counters = []

    def add_counter(self, c):
        # add counter
        print "New Counter being added.."
        # counter = Counter.Counter()
        counter = copy.deepcopy(c)
        self.counters.append(counter)

    def remove_counter(self):
        # remove counter
        print ""

    def get_free_counter(self):
        # get free counter based on flag (busy status)
        print ""
        for c in self.counters:
            if not c.is_busy():
                return c




def main():
    customerQueueFactory = CustomerQueueFactory()
    endpoints.serverFromString(reactor, "tcp:"+str(server.queue['port'])).listen(customerQueueFactory)
    reactor.run()


if __name__ == '__main__':
    main()
__author__ = 'priya'

from twisted.internet import protocol, reactor
from twisted.protocols import basic
from twisted.internet.protocol import ClientFactory
from twisted.internet.defer import Deferred
from Actors.Customer import Customer
import time
import json
from Message import Message


class CounterServerFactory(protocol.Factory):
    def __init__(self):
        print "at server  factory"
        CounterServerProtocol().connectToOtherServer("")
        #time.sleep(3)
        #CounterServerProtocol().connectToAttendantServer("")
        pass

    def buildProtocol(self, addr):
        return CounterServerProtocol()

class CounterServerProtocol(basic.LineReceiver):

    def __init__(self):
        self.queue_factory = CounterClientFactory()
        #self.queue_factory.protocol = CounterClientProtocol
        pass

    def connectionMade(self):
        print("Connection made with Counter Server")
        self.connectToAttendantServer("")

    def dataReceived(self, data):
        print data
        try:
            message = json.loads(data)

            if message['msg_type'] == 'customer':
                self.customer = Customer()
                self.customer.object_decoder(message['payload'])

            elif message['msg_type'] == 'greeting':
                msg = Message('greeting',"M great!!")

            elif message['msg_type'] == 'next_customer':
                # print "Got msg from attendant"
                # #proto = self.queue_factory.protocol
                # #proto.nextCustomer()
                # self.queue_factory.nextCustomer()
                #
                # print "sending msg to attendant"
                # time.sleep(5)
                msg = Message('customer_arrived', "")


            elif message['msg_type'] == 'give_items':
                msg = Message('process_items', self.customer.get_items())


            elif message['msg_type'] == 'show_age_proof':
                msg = Message('age_proof', self.customer.has_age_proof())


            elif message['msg_type'] == 'get_payment':
                if self.customer.hasDebitOrCreditCard:
                    msg = Message('hasDebitOrCreditCard', True)
                else:
                    msg = Message('cashOnHand',self.customer.cashOnHand)


            elif message['msg_type'] == 'insufficient_funds':
                self.customer = None
                msg = Message('reject', True)

            elif message['msg_type'] == 'success':
                msg = Message('complete', True)


            msg_json = json.dumps(msg, default=lambda o: o.__dict__)
            print msg_json
            self.transport.write(msg_json)

        except Exception as e:
            print e.message
            # self.transport.write("Buddy, you screwed up! in AttendantServer:(")
            pass

    def connectToOtherServer(self, line):
        #host, port = line.split()
        #port = int(port)
        print "Connecting to queue server"
        #host = "10.189.146.171"
        host = "localhost"
        port = 1234
        #factory = CounterClientFactory()
        #factory.protocol = CounterClientProtocol
        self.queue_factory.protocol = CounterClientProtocol
        reactor.connectTCP(host, port, self.queue_factory)

    def connectToAttendantServer(self,line):
        print "Connecting to attendant server"
        #host = "10.189.146.171"
        host = "localhost"
        port = 3030
        factory = AttendantClientFactory()
        factory.protocol = AttendantClientProtocol
        reactor.connectTCP(host, port, factory)

class CounterClientProtocol(basic.LineReceiver):

    def connectionMade(self):
        print("Connection made with the Queue Server")
        self.sendLine("{\"msg_type\":\"nextcustomer\"}")
        print("Fetch Customer from queue")

    def nextCustomer(self):
        self.sendLine("{\"msg_type\":\"nextcustomer\"}")
        print("Fetch Customer from queue")

class CounterClientFactory(ClientFactory):
    protocol = CounterClientProtocol()

    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)

class AttendantClientProtocol(basic.LineReceiver):

    def connectionMade(self):
        print("Connection made with Attendant Server")
        #self.sendLine("{\"msg_type\":\"greeting\"}","{\"payload\":\"Hello Attendant!! Morning\"}")

    def dataReceived(self, data):
        print data


class AttendantClientFactory(ClientFactory):
    protocol = AttendantClientProtocol()

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)

def main():
    import sys
    from twisted.python import log

    log.startLogging(sys.stdout)
    factory = CounterServerFactory()
    factory.protocol = CounterServerProtocol
    reactor.listenTCP(1567, factory)
    reactor.run()

if __name__ == '__main__':
    main()

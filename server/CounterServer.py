__author__ = 'priya'

from twisted.internet import protocol, reactor
from twisted.protocols import basic
from twisted.internet.protocol import ClientFactory
from twisted.internet.defer import Deferred
from Actors.Customer import Customer
import json
from Message import Message
from Config import server
import time
global_customer = Customer()
has_customer = False

class CounterServerFactory(protocol.Factory):
    def __init__(self):
        print "at server  factory"
        CounterServerProtocol().connectToOtherServer("")
        pass

    def buildProtocol(self, addr):
        return CounterServerProtocol()


class CounterServerProtocol(basic.LineReceiver):

    def __init__(self):
        self.queue_factory = CounterClientFactory()
        pass

    def connectionMade(self):
        print("Connection made with Counter Server")


    def dataReceived(self, data):
        # print data
        global global_customer
        try:
            message = json.loads(data)

            if message['msg_type'] == 'greeting':
                print message['payload']
                msg = Message('greeting', "M great!! And You?")

            elif message['msg_type'] == 'next_customer':
                self.connectToOtherServer("")
                time.sleep(3)
                # print global_customer
                if not has_customer:
                    msg = Message('no_customer',"No customer in the queue at this moment")
                else:
                    print message['payload']
                    msg = Message('customer_arrived', "")

            elif message['msg_type'] == 'give_items':
                print message['payload']
                msg = Message('process_items', global_customer.get_items())

            elif message['msg_type'] == 'show_age_proof':
                print message['payload']
                msg = Message('age_proof', global_customer.has_age_proof())

            elif message['msg_type'] == 'get_payment':
                print message['payload']
                if global_customer.hasDebitOrCreditCard:
                    msg = Message('process_card', True)
                else:
                    msg = Message('process_cash', global_customer.cashOnHand)

            elif message['msg_type'] == 'insufficient_funds':
                print message['payload']
                #global_customer = None
                msg = Message('reject', "Oops! Sorry. I'll come back again")

            elif message['msg_type'] == 'success':
                print message['payload']
                #global_customer = None
                msg = Message('complete', "Thanks. You too :)")

            else:
                print message['payload']
            msg_json = json.dumps(msg, default=lambda o: o.__dict__)
            # print msg_json
            self.transport.write(msg_json)
            time.sleep(2)

        except Exception as e:
            print e.message
            # self.transport.write("Buddy, you screwed up! in AttendantServer:(")
            pass

    def connectToOtherServer(self, line):

        print "Connecting to queue server"
        host = server.queue['ip']
        port = server.queue['port']
        #factory = CounterClientFactory()
        #factory.protocol = CounterClientProtocol
        self.queue_factory.protocol = CounterClientProtocol
        reactor.connectTCP(host, port, self.queue_factory)


class CounterClientProtocol(basic.LineReceiver):

    def connectionMade(self):
        print("Connection made with the Queue Server")
        self.sendLine("{\"msg_type\":\"nextcustomer\"}")

    def nextCustomer(self):
        self.sendLine("{\"msg_type\":\"nextcustomer\"}")
        print("Fetch Customer from queue")

    def dataReceived(self, data):
        print " Next customer received from Queue Server: " + data
        global global_customer
        global has_customer
        try:
            message = json.loads(data)

            if message['msg_type'] == 'customer':
                has_customer = True
                global_customer = Customer()
                global_customer.object_decoder(message['payload'])

            elif message['msg_type'] == 'no_customer':
                has_customer = False

        except Exception as e:
            print e.message
            # self.transport.write("Buddy, you screwed up! in AttendantServer:(")
            pass


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


def main(port):
    import sys
    from twisted.python import log

    log.startLogging(sys.stdout)
    factory = CounterServerFactory()
    factory.protocol = CounterServerProtocol
    reactor.listenTCP(port, factory)
    reactor.run()

if __name__ == '__main__':
    main(3030)
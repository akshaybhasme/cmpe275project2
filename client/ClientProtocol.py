__author__ = 'jatin'

import sys
from Actors.Customer import Customer
from Models import Item
from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from Message import Message
from threading import Thread
import thread


class ClientProtocol(LineReceiver):
    end = "Bye-bye!"

    def __init__(self):
        self.cg = ClientGenerator(self)

    def connectionMade(self):
        thread.start_new_thread(self.cg.takeUserInput, ())
        print "Connection made"

    def sendMsg(self,msg):
        print("sending customer to queue")
        m = msg.get_message_json()
        print m
        self.sendLine(m)

    def lineReceived(self, line):
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()

    def dataReceived(self, line):
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()


class ClientFactory(ClientFactory):
    protocol = ClientProtocol

    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)


class ClientGenerator:

    def __init__(self, qc):
        print(qc)
        self.protocol = qc
        print("")

    def sendRandomCustomerToQueue(self):
        print("sending it to customer")

    def takeUserInput(self):
        print("--------------------------------------------------------------------------")
        print("-----------------------Welcome to Safeway!!-------------------------------")

        enterOption = input("Press 1 to Enter, Press 2 to Exit")
        if enterOption == 1:
            print("-----------------------------------------------------------------------")
            new_customer = ""
            while True:
                print("-----------------------------------------------------------------------")
                print("Enter 1 for creating a customer")
                print("Enter 2 for generating a random customer")
                print("Enter 3 to exit")
                option = input("Please Enter your choice")
                print("\n")

                if option == 1:
                    new_customer = Customer()
                    del new_customer.items[:]
                    while True:
                        print("Enter 1 for Adding Item")
                        print("Enter 2 to see all the Items")
                        print("Enter 3 If finished shopping")

                        option2 = input("Please Enter your choice")
                        if option2 == 1:
                            item = Item.Item()
                            new_customer.items.append(item)
                            print("---------------------New Item Added-------------------------\n")

                        elif option2 == 2:
                            print("Item Name                    Item Price\n")
                            print("-----------------------------------------")
                            for i in new_customer.items:
                                print(str(i.name)+"                        "+ str(i.value))
                            print("\n")

                        elif option2 ==3:
                            message = Message('addcustomer', new_customer)
                            m = message.get_message_json()
                            self.protocol.sendLine(m)
                            print("Customer sent to the queue")
                            break




                if option==2:
                    message = Message('addcustomer', Customer())
                    m = message.get_message_json()
                    self.protocol.sendLine(m)
                    print("Customer sent to the queue")
                    continue

                if option ==3:
                    break

        if enterOption == 2:
            print("Good Bye")
            sys.exit()


def main(reactor):
    factory = ClientFactory()
    reactor.connectTCP('localhost', 1234, factory)
    return factory.done


if __name__ == '__main__':
    task.react(main)

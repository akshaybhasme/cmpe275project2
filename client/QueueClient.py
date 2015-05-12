__author__ = 'jatin'

import sys
from Actors.Customer import Customer
from Models import Item
from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from Message import Message


class QueueClient(LineReceiver):
    end = "Bye-bye!"

    def __init__(self):
        pass

    def connectionMade(self):
        #print("connection made")
        #message = Message('addcustomer', Customer())
        #m = message.get_message_json()
        #print m
        #self.sendMsg(m)
        #print("customer sent")
        self.cg = ClientGenerator(self)
        self.cg.takeUserInput()

    def sendMsg(self,msg):
        print("send data to customer")
        c = Customer();
        message = Message('addcustomer', c)
        self.sendLine(msg)

    def lineReceived(self, line):
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()

    def dataReceived(self, line):
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()


class ClientFactory(ClientFactory):
    protocol = QueueClient

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
        self.client_sender = qc
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
                print("Enter 1 for Creating Customer")
                print("Enter 2 for Adding Item")
                print("Enter 3 If finished shopping")
                print("Enter 4 for Creating a random customer")
                print("Enter 5 to exit")

                option = input("Please Enter your choice")
                print("\n")

                if option == 1:
                    new_customer = Customer.Customer()
                if option == 2:
                    if new_customer == "":
                        print("Please create a customer first")
                    else:
                        print(new_customer.items)
                if option == 3:
                    #send it to queue
                    new_customer = ""
                if option == 4:
                    print("reached 4")
                    print(self.client_sender)
                    self.client_sender

                if option == 5:
                    sys.exit()

        if enterOption == 2:
            sys.exit()


def main(reactor):
    factory = ClientFactory()
    reactor.connectTCP('10.189.71.128', 1234, factory)
    return factory.done


if __name__ == '__main__':
    task.react(main)

# __author__ = 'sid'
#
# from Actors import Customer, Attendant
# import Models.Item as Item
# import Message
# import json
#from twisted.internet import protocol, reactor, endpoints
#
# class AttendantServer(protocol.Protocol):
#     def __init__(self):
#         self.att = Attendant()
#         self.items = Item()
#
#     def dataReceived(self, data):
#         total = 0
#         alcoholic = False
#         try:
#             message = json.loads(data)
#             if message['type'] == 'process_items':
#                 self.items = message['items']
#                 i = None
#                 for i in self.items:
#                     if i.is_alcoholic():
#                         alcoholic = True
#                         total = total + i.get_value()
#
#                 if alcoholic:
#                     msg = Message('get_age_proof', self.customer)
#                     self.transport.write(json.dumps(msg, default=lambda o: o.__dict__))
#
#             elif message['type'] == 'age_proof':
#                 age_proof = message['hasAgeProof']
#                 if age_proof:
#                     msg = Message('get_payment', self.customer)
#                     self.transport.write(json.dumps(msg, default=lambda o: o.__dict__))
#
#             elif message['type'] == 'process_payment':
#                 payment = message['hasDebitOrCreditCard']
#                 if payment:
#                     msg = Message('success', self.customer)
#                     self.transport.write(json.dumps(msg, default=lambda o: o.__dict__))
#                 else:
#                     msg = Message('cash', self.customer)
#                     self.transport.write(json.dumps(msg, default=lambda o: o.__dict__))
#
#             elif message['type'] == 'process_cash':
#                 cash = message['cashOnHand']
#                 if cash < total:
#                     msg = Message('success', self.customer)
#                     self.transport.write(json.dumps(msg, default=lambda o: o.__dict__))
#         except:
#             # print exception here if you want a debug statement
#             pass
#
# class AttendantFactory(protocol.Factory):
#     def __init__(self):
#         pass
#
#     def buildProtocol(self, addr):
#         return AttendantServer()
#
# class AttendantServerProtocol(basic.)

from twisted.internet import protocol, reactor
from twisted.protocols import basic
from twisted.internet.protocol import ClientFactory
from twisted.internet.defer import Deferred


class AttendantServerFactory(protocol.Factory):
    def __init__(self):
        print "at server  factory"
        AttendantServerProtocol().connectToOtherServer("")
        pass

    def buildProtocol(self, addr):
        return AttendantServerProtocol()

class AttendantServerProtocol(basic.LineReceiver):

    def __init__(self):
        pass

    def connectionMade(self):
        print("connection made")

    def connectToOtherServer(self, line):
        #host, port = line.split()
        #port = int(port)
        print "connect to other server"
        host = "10.189.235.131"
        port = 1234
        factory = AttendantClientFactory()
        factory.protocol = AttendantClientProtocol
        reactor.connectTCP(host, port, factory)


class AttendantClientProtocol(basic.LineReceiver):

    def connectionMade(self):
        print("connection made")
        self.sendLine("hello Priya")
        print("customer sent")


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
    factory = AttendantServerFactory()
    factory.protocol = AttendantServerProtocol
    reactor.listenTCP(1234, factory)
    reactor.run()

if __name__ == '__main__':
    main()

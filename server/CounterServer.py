__author__ = 'priya'

from twisted.internet import protocol, reactor
from twisted.protocols import basic
from twisted.internet.protocol import ClientFactory
from twisted.internet.defer import Deferred

class CounterServerFactory(protocol.Factory):
    def __init__(self):
        print "at server factory"
        CounterServerProtocol().connectToOtherServer("")
        pass

    def buildProtocol(self, addr):
        return CounterServerProtocol()

class CounterServerProtocol(basic.LineReceiver):

    def __init__(self):
        pass

    def connectionMade(self):
        print("connection made")

    def connectToOtherServer(self, line):
        #host, port = line.split()
        #port = int(port)
        print "connect to other server"
        host = "10.189.71.128"
        port = 1234
        factory = CounterClientFactory()
        factory.protocol = CounterClientProtocol
        reactor.connectTCP(host, port, factory)

class CounterClientProtocol(basic.LineReceiver):

    def connectionMade(self):
        print("connection made")
        self.sendLine("{\"type\":\"addcustomer\"}")
        print("customer sent")

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

def main():
    import sys
    from twisted.python import log

    log.startLogging(sys.stdout)
    factory = CounterServerFactory()
    factory.protocol = CounterServerProtocol
    reactor.listenTCP(1234, factory)
    reactor.run()

if __name__ == '__main__':
    main()

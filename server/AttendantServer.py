__author__ = 'sid'


from Actors import Attendant
import Message
import json
from twisted.internet import protocol, reactor, endpoints
from twisted.protocols import basic
from twisted.internet.protocol import ClientFactory
from twisted.internet.defer import Deferred


class AttendantServer(protocol.Protocol):
    def __init__(self):
        self.attendant = Attendant()

    def dataReceived(self, data):
        total = 0
        alcoholic = False
        msg_txt = None
        print data
        try:
            message = json.loads(data)

            if message['type'] == 'process_items':
                items = message['items']
                alcoholic = self.attendant.process_item_list(items)
                if alcoholic:
                    msg_txt = 'get_age_proof'

            elif message['type'] == 'age_proof':
                age_proof = message['hasAgeProof']
                if not age_proof:
                    self.attendant.remove_alcoholic()
                msg_txt = 'get_payment'

            elif message['type'] == 'process_card':
                has_card = message['hasDebitOrCreditCard']
                payment = 0
                if has_card:
                    msg_txt = 'success'
                else:
                    msg_txt = 'failure'

            elif message['type'] == 'process_cash':
                cash = message['cashOnHand']
                payment = self.attendant.process_cash(cash)
                if payment:
                    msg_txt = 'success'
                else:
                    msg_txt = 'failure'

            msg = Message(msg_txt, self.customer)
            msg_json = json.dumps(msg, default=lambda o: o.__dict__)
            print msg_json
            self.transport.write(msg_json)

        except Exception as e:
            print e.message
            self.transport.write("Buddy, you screwed up! in AttendantServer:(")
            pass


class AttendantServerFactory(protocol.Factory):
    def __init__(self):
        print "at attendant server factory"
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
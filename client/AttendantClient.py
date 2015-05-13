__author__ = 'sid'


from Actors import Attendant
from Message import Message
import json
import time
from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from Models.Item import Item

from twisted.internet.defer import Deferred

class AttendantClientProtocol(LineReceiver):

    def __init__(self):
        self.attendant = Attendant.Attendant()

    def connectionMade(self):
        print("connection made in attendant client")
        self.sendLine(("{\"msg_type\":\"next_customer\"}"))

    def dataReceived(self, data):
        total = 0
        alcoholic = False
        print data
        try:
            message = json.loads(data)
            # print("Message received")
            if message['msg_type'] == 'customer_arrived':
                msg = Message('greeting', 'Hello, how are you doing?')

            elif message['msg_type'] == 'greeting':
                msg = Message('give_items', "")

            elif message['msg_type'] == 'no_customer':
                print("Haila, No Customer!!")
                time.sleep(2)
                msg = Message('next_customer', 'soon')

            elif message['msg_type'] == 'process_items':
                items = []
                for i in message['payload']:
                    item = Item()
                    item.decode_from_json(i)
                    items.append(item)
                alcoholic = self.attendant.process_item_list(items)
                if alcoholic:
                    msg = Message('show_age_proof',"")

            elif message['msg_type'] == 'age_proof':
                age_proof = message['payload']
                if not age_proof:
                    self.attendant.remove_alcoholic()
                msg = Message('get_payment',"")

            elif message['msg_type'] == 'process_card':
                has_card = message['payload']
                payment = 0
                if has_card:
                    msg = Message('success',"")
                else:
                    msg = Message('failure',"")

            elif message['msg_type'] == 'process_cash':
                cash = message['payload']
                payment = self.attendant.process_cash(cash)
                if payment:
                    msg = Message('success',"")
                else:
                    msg = Message('insufficient_funds',"")

            elif message['msg_type'] == 'complete' or message['msg_type'] == 'reject':
                self.attendant.become_idle()
                msg = Message('next_customer',"")

            else:
                msg = Message('none of these satisfied', "")

            msg_json = json.dumps(msg, default=lambda o: o.__dict__)
            # print msg_json
            #self.transport.write(msg_json)
            self.sendLine(msg_json)

        except Exception as e:
            print e.message
            self.transport.write("Buddy!, I screwed up! in AttendantServer:(")
            pass


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


def main(reactor, ip, port):

    factory = AttendantClientFactory()
    factory.protocol = AttendantClientProtocol
    reactor.connectTCP(ip, port, factory)
    return factory.done

if __name__ == '__main__':
    task.react(main('10.189.235.131', 3030))

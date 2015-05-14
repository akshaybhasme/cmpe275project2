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
        # print data
        try:
            message = json.loads(data)
            # print("Message received")
            if message['msg_type'] == 'customer_arrived':
                # print message['payload']
                msg = Message('greeting', 'Hello, how are you doing today?')

            elif message['msg_type'] == 'greeting':
                print message['payload']
                msg = Message('give_items', "I'm doing good.Thank you.\nCould you pass along all the items?")

            elif message['msg_type'] == 'no_customer':
                # this payload does not need to be printed in the final deliverable
                # print message['payload']
                time.sleep(2)
                msg = Message('next_customer', 'Next in line?')

            elif message['msg_type'] == 'process_items':
                items = []
                for i in message['payload']:
                    time.sleep(1)
                    item = Item()
                    item.decode_from_json(i)
                    print item.get_name(),"\t", item.get_value(),"\t Alcolholic? ",item.is_alcoholic()
                    items.append(item)
                alcoholic = self.attendant.process_item_list(items)
                if alcoholic:
                    msg = Message('show_age_proof', "I need to see your ID for the alcoholic item")
                else:
                    result = self.attendant.get_total()
                    msg = Message('get_payment', result)

            elif message['msg_type'] == 'age_proof':
                age_proof = message['payload']
                result = ''
                if not age_proof:
                    print "Sorry I don't have an Age-Proof document with me right now."
                    result += str(self.attendant.remove_alcoholic())
                else:
                    print "Here you go"
                # need to display amount now
                result += str(self.attendant.get_total())
                msg = Message('get_payment', result)

            elif message['msg_type'] == 'process_card':
                print message['payload']
                result = self.attendant.process_card()
                msg = Message('success', result)

            elif message['msg_type'] == 'process_cash':
                cash = message['payload']
                print("Here's $", str(cash), "for the bill")
                payment = self.attendant.process_cash(cash)
                success = self.attendant.get_total_amount()
                print "success ", success
                if success <= 0:
                    msg = Message('success', payment)
                else:
                    msg = Message('insufficient_funds', payment)

            elif message['msg_type'] == 'complete' or message['msg_type'] == 'reject':
                print message['payload']
                self.attendant.become_idle()
                msg = Message('next_customer', "next customer in line please")

            else:
                print message['payload']
                msg = Message('oops', "none of these conditions satisfied")

            msg_json = json.dumps(msg, default=lambda o: o.__dict__)
            self.sendLine(msg_json)
            time.sleep(2)

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
    task.react(main, ["localhost", 3030])

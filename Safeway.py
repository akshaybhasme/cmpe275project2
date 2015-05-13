__author__ = 'apurvapawar'

import sys

from client import CustomerGenerator
from client import AttendantClient
from server import CounterServer
from server import CustomerQueueServer

from client.AttendantClient import AttendantClientFactory
from client.AttendantClient import AttendantClientProtocol


def main():
    options = {"queue": queue, "attendant": attendant, "counter": counter, "generator": generator}
    if options.get(sys.argv[1]) is None:
        print "Invalid Arguments Entered."
        sys.exit(0)
    else:
        options.get(sys.argv[1])()


def queue():
    # start attendant server
    print "Starting Safeway Shop Queue..."
    CustomerQueueServer.main()


def attendant():
    check_arguments_for_attendant()
    print "Starting Safeway Attendant..."
    # start attendant server
    #
    # def start(reactor):
    #     factory = AttendantClientFactory()
    #     factory.protocol = AttendantClientProtocol
    #     reactor.connectTCP(sys.argv[2], sys.argv[3], factory)
    #     return factory.done
    # AttendantClient.task.react(start)

    AttendantClient.task.react(AttendantClient.main, [sys.argv[2], sys.argv[3]])


def counter():
    check_second_argument()
    print "Starting Safeway Counter..."
    # start counter server
    CounterServer.main(int(sys.argv[2]))


def generator():
    print "Starting Safeway Customer Generator..."
    # start customer generator
    CustomerGenerator.task.react(CustomerGenerator.main)


def is_int_string(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def check_second_argument():
    if len(sys.argv) < 3:
        print "Please enter port number second argument."
        sys.exit(0)

    if not is_int_string(sys.argv[2]):
        print "Second argument should be of type integer for port number."
        sys.exit(0)


def check_arguments_for_attendant():
    if len(sys.argv) < 4:
        print "Please enter correct set of arguments (ip, port) for attendant."
        sys.exit(0)

    if not is_int_string(sys.argv[3]):
        print "Third argument should be of type integer for port number."
        sys.exit(0)


if __name__ == '__main__':
    main()
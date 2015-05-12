__author__ = 'apurvapawar'

import sys

from client import ClientProtocol
from server import AttendantServer
from server import CounterServer
from server import CustomerQueueServer


def main():
    options = {"queue": queue, "attendant": attendant, "counter": counter, "generator": generator}
    if options.get(sys.argv[1]) is None:
        print "Invalid Arguments Entered."
        sys.exit(0)
    else:
        options.get(sys.argv[1])()


def queue():
    # if len(sys.argv) < 3:
    #     print "Please enter number of counters as second argument for argument 'shop'"
    #     sys.exit(0)
    #
    # if not is_int_string(sys.argv[2]):
    #     print "Second argument should be of type integer for argument 'shop'"
    #     sys.exit(0)
    #
    # number_of_counters = int(sys.argv[2])
    #
    # print "Starting Shop with "+str(number_of_counters)+" Counters..."
    # start shop server with above number of counters
    print "Starting Safeway Shop Queue..."
    CustomerQueueServer.main()


def attendant():
    print "Starting Safeway Attendant..."
    # start attendant server
    AttendantServer.main()


def counter():
    print "Starting Safeway Counter..."
    # start counter server
    CounterServer.main()


def generator():
    print "Starting Safeway Customer Generator..."
    # start customer generator
    ClientProtocol.task.react(ClientProtocol.main)


def is_int_string(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    main()
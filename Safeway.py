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
    # start attendant server
    print "Starting Safeway Shop Queue..."
    CustomerQueueServer.main()


def attendant():
    check_second_argument()
    print "Starting Safeway Attendant..."
    # start attendant server
    AttendantServer.main(sys.argv[2])


def counter():
    check_second_argument()
    print "Starting Safeway Counter..."
    # start counter server
    CounterServer.main(sys.argv[2])


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


def check_second_argument():
    if len(sys.argv) < 3:
        print "Please enter port number second argument."
        sys.exit(0)

    if not is_int_string(sys.argv[2]):
        print "Second argument should be of type integer for port number."
        sys.exit(0)


if __name__ == '__main__':
    main()
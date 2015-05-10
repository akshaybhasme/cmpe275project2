__author__ = 'apurvapawar'

import sys


def main():
    options = {"shop": shop, "attendant": attendant, "counter": counter}
    if options.get(sys.argv[1]) is None:
        print "Invalid Arguments Entered."
        sys.exit(0)
    else:
        options.get(sys.argv[1])()


def shop():
    if len(sys.argv) < 3:
        print "Please enter number of counters as second argument for argument 'shop'"
        sys.exit(0)

    if not is_int_string(sys.argv[2]):
        print "Second argument should be of type integer for argument 'shop'"
        sys.exit(0)

    number_of_counters = int(sys.argv[2])

    print "Starting Shop with "+str(number_of_counters)+" Counters..."
    # start shop server with above number of counters


def attendant():
    print "Starting Attendant..."
    # start attendant server


def counter():
    print "Starting Counter..."
    # start counter server


def is_int_string(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    main()
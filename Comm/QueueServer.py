__author__ = 'akshaybhasme'


import socket
import Actors

s = socket.socket()
host = s.gethostname()
port = 5555

s.bind((host, port))

s.listen(5)

q = Actors.CustomerQueue()

while True:
    c, addr = s.accept()
    c.send("Thanks")
    c.close()
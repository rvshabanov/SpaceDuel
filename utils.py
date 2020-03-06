import os
import sys
import socket


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


class LanServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.c = None
        self.caddr = None
        self.buff = None

        self.s = socket.socket()
        self.s.bind((host, port))

        self.s.listen(5)

    def listen(self):
        self.c, self.caddr = self.s.accept()
        print('Got connection from', self.caddr)
        self.c.send('Thank you for connecting')

    def close(self):
        self.s.close()


class LanClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buff = None

        self.s = socket.socket()
        self.s.connect((host, port))

    def recv(self):
        self.buff = self.s.recv(1024)
        print('CLIENT RECV: ' + self.buff)

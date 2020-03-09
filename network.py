# Imports
import socket

# My imports
import constants


class Network:
    def __init__(self, host):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = host
        self.port = constants.LAN_PORT
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print("Connect failed: ", e)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return 0, self.client.recv(2048).decode()
        except socket.error as e:
            return e, 0


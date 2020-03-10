# Credits to Tim for the server-client concept
# https://techwithtim.net/
# https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg

# Import modules
import socket

# My imports
import constants


class Network:
    """
    Class Network
    Handles client side of LAN game

    Init - init Network instance
            parameters:
            host - hostname | IP of the server to connect to
    """
    def __init__(self, host):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = host
        self.port = constants.LAN_PORT
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    """
    Connect - connect to server
            parameters:
            none
    """
    def connect(self):
        # Try to connect to the server and return the response
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print("Connect failed: ", e)        # Just print error if any

    """
    Send - send data to server and get the reply
            parameters:
            data - string containing data
            returns:
            tuple (e, data), where e - error or 0, data - string with server response data
    """
    def send(self, data):
        # Try to send data and get the reply
        try:
            self.client.send(str.encode(data))
            return 0, self.client.recv(2048).decode()   # return no error, response
        except socket.error as e:
            return e, ""                                # return error, empty string as response

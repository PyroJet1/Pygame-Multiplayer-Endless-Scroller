import socket

class Network:
    def __init__(self, id):
        self.id = id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

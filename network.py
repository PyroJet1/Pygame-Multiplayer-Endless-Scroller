import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "130.37.61.243"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()


    def connect(self):
        self.client.connect(self.addr)

        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass


import socket
import pickle


class Network:
    def __init__(self, pname):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect(pname)

    def getP(self):
        return self.p

    def connect(self, pname):
        try:
            self.client.connect(self.addr)
            self.client.send(str.encode(pname))
            return pickle.loads(self.client.recv(2048*2))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)


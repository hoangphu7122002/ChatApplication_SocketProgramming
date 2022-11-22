from socket import *
from threading import *

PORT = 1234
# host name of peer1
HOST = gethostname()

print(HOST)

class ChatThread(Thread):
    def __init__(self,conn,name):
        Thread.__init__(self)
        self.conn = conn
        self.name = name
    def run(self):
        while True:
            if self.name == 'Sender':
                data = input('')
                self.conn.send(data.encode())
            elif self.name == 'Receiver':
                recData = self.conn.recv(1024).decode()
                print('=> {}'.format(recData))
        
client = socket()
client.connect((HOST, PORT))

sender = ChatThread(client, 'Sender')
receiver = ChatThread(client, 'Receiver')
sender.start()
receiver.start()
# sender.join()
# receiver.join()
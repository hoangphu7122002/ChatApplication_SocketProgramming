from socket import *
from threading import *

class ChatThread(Thread):
    def __init__(self,conn):
        Thread.__init__(self)
        self.conn = conn
    def run(self):
        while True:
            name = current_thread().getName()
            if name == 'Sender':
                data = input('')
                self.conn.send(data.encode())
            elif name == 'Receiver':
                recData = self.conn.recv(1024).decode()
                print('=>: {}'.format(recData))
        
client = socket()
client.connect(('127.0.0.1',1234))

sender = ChatThread(client)
sender.setName('Sender')
receiver = ChatThread(client)
receiver.setName('Receiver')
sender.start()
receiver.start()
# sender.join()
# receiver.join()
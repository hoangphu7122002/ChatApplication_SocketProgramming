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
                print('=> {}'.format(recData))
        
server = socket(AF_INET,SOCK_STREAM)
server.bind(('127.0.0.1',1234))
server.listen(4)
connection, address = server.accept()

sender = ChatThread(connection)
sender.setName('Sender')
receiver = ChatThread(connection)
receiver.setName('Receiver')
sender.start()
receiver.start()
# sender.join()
# receiver.join()
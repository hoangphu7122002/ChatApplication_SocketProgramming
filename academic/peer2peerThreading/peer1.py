from socket import *
from threading import *

# HOST = gethostname()
PORT = 1234

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
        
server = socket(AF_INET,SOCK_STREAM)
server.bind(('', PORT))
server.listen()
connection, address = server.accept()

sender = ChatThread(connection, 'Sender')
receiver = ChatThread(connection,'Receiver')
sender.start()
receiver.start()
# sender.join()
# receiver.join()
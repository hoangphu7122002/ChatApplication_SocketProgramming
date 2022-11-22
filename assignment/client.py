import socket
from threading import *
from user import *
from hyper_parameter import *
import pickle
import errno
import sys
from time import time

dict_map_type = {
    '1' : 'listUser',
    '2' : 'connectUser',
    '3' : 'listGroup',
    '4' : 'connectGroup',
    '5' : 'quit'
}

class ChatThread(Thread):
    def __init__(self,client_socket,name):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.name = name
        
    def run(self):
        pass
    
class Client(User):
    def __init__(self):
        super().__init__()
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1",1234))
        
    def client_obj_send(self,obj_message):
        if type(obj_message) == str:
            obj_msg = self.get_info().copy()
            obj_msg["type"] = "msg"
            obj_msg["message"] = obj_message            
            obj_message = obj_msg
            
        msg = pickle.dumps(obj_message)
        msg = bytes(f"{len(msg):<{HEADER_LENGTH}}","utf-8") + msg
        return msg        
    
    def sign_in(self):
        self.user_name = input("please input username: ")
        self.password = input("please input password: ")
        self.client.send(self.client_obj_send(self.get_info()))
        header_length = None
        while header_length == None:
            # add time prevent case server expired
            header_length = self.client.recv(HEADER_LENGTH)
        message_length = int(header_length.decode("utf-8").strip())
        data_res = self.client.recv(message_length)
        data = pickle.loads(data_res)
        if data["message"] == "login fail":
            print("username or password is incorrect!!!")
            self.client.close()
            return False
        print(data)
        return True
    
    def peer(self):
        pass
    
    def run(self):
        if self.sign_in() == True:
            #push history
            print("choose option:")
            print("==========================================")
            print("list all user connection - 1")
            print("connect with user - 2") #peer2peer here
            print("list all group connection - 3") #broadcast data here
            print("connect with group - 4") #client2sever
            print("quit - 5")
            print("==========================================")
            while True:
                n = '6'
                while n not in ['1','2','3','4','5']:
                    n = input(f"{self.user_name} > ")
                option_info = {"user_name" : self.user_name,"type" : dict_map_type[n], "message" : ''}
                self.client.send(self.client_obj_send(option_info))
                try:
                    while True:
                        server_length = self.client.recv(HEADER_LENGTH)
                        if not len(server_length):
                            print("connection closed by server")
                            sys.exit()
                        server_length = int(server_length.decode('utf-8').strip())
                        data_server = self.client.recv(server_length)
                        data_server = pickle.loads(data_server)
                        print("Server:>")
                        print(data_server)
                        break
                except IOError as e:
                    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                        print('Reading error',str(e))
                        sys.exit() 
                    continue
                except Exception as e:
                    print('General error',str(e))
                    sys.exit()
    
if __name__ == "__main__":
    client = Client()
    client.run()
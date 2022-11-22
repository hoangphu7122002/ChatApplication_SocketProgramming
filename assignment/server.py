import socket
import threading
from hyper_parameter import *
import select
import pickle

class Server:
    def __init__(self,ip_host,port):
        self.ip_host = ip_host
        self.port = port
        
    def listen(self):
        self.server_side = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_side.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server_side.bind((self.ip_host,self.port))
        self.sockets_list = [self.server_side]
        self.clients = {}
        self.clients_banded =  {}
        
        print("Server is active:")
        self.server_side.listen(QUEUE_CLIENT) #can modify this variable
    
    def server_message(self,obj_send):
        msg = pickle.dumps(obj_send)
        msg = bytes(f"{len(msg):<{HEADER_LENGTH}}","utf-8") + msg
        return msg
    
    def auth_message(self,client_socket):
        try:
            message_header = client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                return False
            message_length = int(message_header.decode("utf-8").strip())
            return {"header" : message_header, "data" : client_socket.recv(message_length)}
        except:
            return False
    
    def check_auth(self,auth):
        for usr in list_user:
            flag = True
            if auth["user_name"] != usr["user_name"]: flag = False
            if auth["password"] != usr["password"]: flag = False
            if flag == True: return True
        return False
        
    def retrieve_info(self):
        self.user_online = []
        for key,val in self.clients.items():
            if val == 1:
                self.user_online.append(key)
        
    def conservation(self,client_socket):
        client_socket.send(self.server_message(auth_success))
        while True:
            try:
                message_header = client_socket.recv(HEADER_LENGTH)
                if not len(message_header):
                    return False
                message_length = int(message_header.decode("utf-8").strip())
                data_user = client_socket.recv(message_length)
                data_user = pickle.loads(data_user)
                #======================IMPLEMENT HERE=======================
                if data_user["type"] == 'listUser':
                    self.retrieve_info()
                    client_socket.send(self.server_message({
                        "user_name" : "Server",
                        "type" : "list",
                        "user_list" : self.user_online
                    }))
                elif data_user["type"] == 'connectUser':
                    client_socket.send(self.server_message({
                        "user_name" : "Server",
                        "type" : "connect",
                        "message" : {
                            "port" : 123,
                            "port" : 347
                        }
                    }))
                elif data_user["type"] == 'quit':
                    client_socket.send(self.server_message({
                        "user_name" : "Server",
                        "type" : "out",
                        "message" : "close connection"
                    }))
                else:
                    client_socket.send(self.server_message({
                        "user_name" : "Server",
                        "type" : "not supported",
                    }))
                #===========================================================
            except Exception as e:
                print(e)
                break
        client_socket.close()
    
    def run(self):
        while True:
            client_socket, client_address = self.server_side.accept()
            #============authentication process===================
            auth = self.auth_message(client_socket)
            if auth == False:
                continue
            data_auth = pickle.loads(auth["data"])
            num_ban = self.clients_banded.get(data_auth["user_name"],0)
            if self.clients.get(data_auth["user_name"],0) == 1:
                print("connection exist!!! from {},{} with username: {}".format(client_address[0],client_address[1],data_auth["user_name"]))
                client_socket.send(self.server_message(auth_already))
                continue
            if num_ban >= 5:
                print("refuse connection!!! from {},{} with username: {}".format(client_address[0],client_address[1],data_auth["user_name"]))
                client_socket.send(self.server_message(auth_fail))
                continue
            if self.check_auth(data_auth) == False:
                self.clients_banded[data_auth["user_name"]] = self.clients_banded.get(data_auth["user_name"],0) + 1
                print("refuse connection!!! from {},{} with username: {}".format(client_address[0],client_address[1],data_auth["user_name"]))
                client_socket.send(self.server_message(auth_fail))
                continue
            self.clients[data_auth["user_name"]] = 1
            print("Connection from {} has been established!!!".format(client_address))
            #============authentication process===================
            t=threading.Thread(target = self.conservation,args=(client_socket,))
            t.start()
        
if __name__ == "__main__":
    server = Server("127.0.0.1",int("1234"))
    server.listen()
    server.run()
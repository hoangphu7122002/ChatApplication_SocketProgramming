import socket
from threading import *
from user import *
from hyper_parameter import *
import pickle
import signal
import sys
from helper_function import *
    
name = sys.argv[1]
our_port = int(sys.argv[2])
p2p_server_addr = sys.argv[3]
p2p_server_port = int(sys.argv[4])

peer_list = []
my_id_peer = None

#to connect server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((p2p_server_addr,p2p_server_port))

def send_client_message(obj_message):
    msg = pickle.dumps(obj_message)
    msg = bytes(f"{len(msg):<{HEADER_LENGTH}}","utf-8") + msg
    return msg   
    
def get_client_data(server):
    header_length = server.recv(HEADER_LENGTH)
    message_length = int(header_length.decode("utf-8").strip())
    data_res = server.recv(message_length)
    data_res = pickle.loads(data_res)
    
    return data_res
    
def is_command(msg, str_cmd):
    return msg.count(str_cmd)    
    
#Handler CTRL+C - Close connection with server
def signal_handler(sig, frame):
    pass

def connect_server():
    password = input('>password:')
    message = {}
    message["user_name"] = name
    message["password"] = password
    message["type"] = AUTHENTICATION
    server.send(send_client_message(message))
    
    print("wait to connect server")
    data_auth = get_client_data(server)
    if data_auth["user_name"] != "SERVER" or data_auth["type"] != AUTH_PROTOCOL_SUCCESS:
        print("close connection!!!")
        server.close()
        return False
    return True
    
def thread_server_read():
    while True:
        global peer_list
        global my_id_peer

        msg = input('>:')
        if is_command(msg,'/quit'):
            message_request = {}
            message_request["type"] = CHAT_PROTOCOL_BYE
            message_request["peer_name"] = name
            message_request["port"] = our_port
            message_request["id_peer"] = my_id_peer
            server.send(send_client_message(message_request))
        if is_command(msg,'/update'):
            message_request = {}
            message_request["type"] = CHAT_PROTOCOL_UPDATE
            message_request["peer_name"] = name
            message_request["port"] = our_port
            message_request["id_peer"] = my_id_peer
            server.send(send_client_message(message_request))
        if is_command(msg,'/help'):
            print_help(name)
        if is_command(msg,'/show_connection'):
            pass
        if is_command(msg,'/show_peers'):
            
            print("test: ",peer_list)
            print_peer_table(name, peer_list) 
        else:
            pass
        
def thread_server_listen():
    while True:
        try:
            data = get_client_data(server)
            if data:
                if data["type"] == CHAT_PROTOCOL_HI_ACK:

                    global peer_list 
                    peer_list = data["peer_list"]
                    global my_id_peer 
                    my_id_peer = data["id_peer"]
                    print("peer_list: ", peer_list)
                    print("my id peer: ", my_id_peer)
                    print('Server:> the list of peers was received correctly, '+str(len(peer_list))+' total active peers')
                if data["type"] == CHAT_PROTOCOL_BYE_ACK:
                    server.close()
                    print("Server:> Closing connections with server.......")
                    print('\n\nGoodbye '+name+'!\n')
                    input("Press Enter to continue...")
                    sys.exit(0)
                if data["type"] == CHAT_PROTOCOL_UPDATE_ACK:
                    peer_list = data["peer_list"]
                    print('Server:> the list of peers was received correctly, '+str(len(peer_list))+' total active peers')
            else:
                server.close()
                print("Goodbye!!!")
        except:
            server.close()
            print("Goodbye!!!")
        
def thread_client():
    while True:
        #---------
        #box
        pass
    
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print('Error: usage: ./' + sys.argv[0] + ' <username> <your_listen_port> <IP_P2P_server> <Port>')
        sys.exit(0)
    #handel Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    if connect_server():
        message_first = {}
        message_first["type"] = CHAT_PROTOCOL_HI
        message_first["peer_name"] = name
        message_first["port"] = our_port
        
        server.send(send_client_message(message_first))
        server_listen = Thread(target= thread_server_listen)
        server_read = Thread(target= thread_server_read)
        server_listen.start()
        server_read.start()
    else:
        print("connection fail, please reset desktop!!")
        
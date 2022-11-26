import socket
from threading import *
from hyper_parameter import *
import pickle
import signal
import sys
from helper_function import *
import time    
    
name = sys.argv[1]
our_port = int(sys.argv[2])
p2p_server_addr = sys.argv[3]
p2p_server_port = int(sys.argv[4])
#to modify later
my_ip_addr = '127.0.0.1'

peer_list = []
my_id_peer = None

#to connect server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((p2p_server_addr,p2p_server_port))

ours_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ours_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
ours_server.bind(('',our_port))
ours_server.listen(QUEUE_CLIENT)

def get_peer_element(peer_list, my_peer_id):
    for peer in peer_list:
        if peer[3] is my_peer_id:
            return peer    

def is_already_Connected(active_conn, id_peer):    
    for conn in active_conn:
        if conn[3] is id_peer:
            return True
    return False
    
def get_sockpeer_element(active_conn_sock, id_to_find):
    for conn in active_conn_sock:
        if conn[0][3] is id_to_find:
            return conn[1]    
        
def getPeerId(msg):
    try:
        return int(msg.split(' ')[1])
    except:
        return 0

def get_msg_to_send(msg):
    text_l = msg.split(' ')
    message = ''
    for i in range(2,len(text_l)):
        message = message + text_l[i]
        if i != len(text_l) - 1:
            message = message + ' '
    return message

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
    
#thread our_server    
active_conn = []
active_conn_sock = []    
socket_peer_list = []     
    
def thread_read():
    while True:
        global peer_list
        global my_id_peer
        global socket_peer_list

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
            print_conn_table(name,active_conn)
        if is_command(msg,'/show_peers'):
            print_peer_table(name, peer_list) 
        if is_command(msg,'/connection'):
            #to connect with someone
            peer_to_connect = []
            id_to_connect = getPeerId(msg)
            if not is_already_Connected(active_conn,id_to_connect) and id_to_connect != 0:
                try:
                    peer_to_connect = get_peer_element(peer_list,id_to_connect)
                    aux_peer = socket.socket((peer_to_connect[2],peer_to_connect[1])) #aka: port, hostname
                    socket_peer_list.append(aux_peer)
                    print("connect with {} is established".format(peer_to_connect[0]))
                    time.sleep(1)
                    message_request = {}
                    message_request["type"] = CHAT_PROTOCOL_CONNECT
                    message_request["peer_name"] = name
                    message_request["port"] = our_port
                    message_request["ip_peer"] = my_ip_addr
                    message_request["id_peer"] = my_id_peer
                    aux_peer.send(send_client_message(message_request))
                except:
                    print("id_peer: {} not found...".format(id_to_connect))
                    continue
        if is_command(msg,'/dis_connection'):
            #to disconnect with someone
            aux_peer = []
            peer_to_dis = []
            id_to_dis = getPeerId(msg)
            if is_already_Connected(active_conn,id_to_dis):
                try:
                    aux_peer = get_sockpeer_element(active_conn_sock, id_to_dis)
                    peer_to_dis = get_peer_element(active_conn, id_to_dis)
                    print("disconnect with {}".format(peer_to_dis[0]))
                    time.sleep(1)
                    message_request = {}
                    message_request["type"] = CHAT_PROTOCOL_DIS
                    message_request["peer_name"] = name
                    message_request["port"] = our_port
                    message_request["ip_peer"] = my_ip_addr
                    message_request["id_peer"] = my_id_peer
                    aux_peer.send(send_client_message(message_request))
                except:
                    print("id_peer: {} not found...".format(id_to_dis))
                    continue
            else:
                print("id_peer: {} not found...".format(id_to_dis))
        if is_command(msg,'/msg'):
            #to communication with each other
            msg_to_send = get_msg_to_send(msg)
            try:
                id_peer_to_send = getPeerId(msg)
                if is_already_Connected(active_conn_sock,id_peer_to_send):
                    peer_to_send = get_sockpeer_element(active_conn_sock,id_peer_to_send)
                    message_request = {}
                    message_request["type"] = CHAT_PROTOCOL_MSG
                    message_request["peer_name"] = name
                    message_request["port"] = our_port
                    message_request["ip_peer"] = my_ip_addr
                    message_request["id_peer"] = my_id_peer
                    message_request["message"] = msg_to_send
                    peer_to_send.send(send_client_message(message_request))
                    print('{}@{}:>{}'.format(name,get_peer_element(peer_list,id_peer_to_send)[0],msg_to_send))
                else:
                    print("id_peer: {} not found...".format(id_peer_to_send))
            except:
                print("invalid id peer")
        else:
            pass
        
def thread_server_listen():
    while True:
        try:
            data = get_client_data(server)
            if data:
                if data["type"] == CHAT_PROTOCOL_HI_ACK:

                    global peer_list 
                    global my_id_peer  
                    peer_list = data["peer_list"]
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
                break
        except:
            server.close()
            print("Goodbye!!!")
            break

def thread_our_server_listen():
    while True:
        global socket_peer_list
        conn, addr = ours_server.accept()
        socket_peer_list.append(conn)
        for peer in socket_peer_list:
            global active_conn
            global active_conn_sock
            if (peer != server) and (peer != ours_server):
                data = get_client_data(peer)
                if data:
                    if data["type"] == CHAT_PROTOCOL_CONNECT:
                        sock_and_conn = []
                        active_conn.append([data["peer_name"],data["port"],data["ip"],data["id_peer"]])
                        sock_and_conn.append([data["peer_name"],data["port"],data["ip"],data["id_peer"]])
                        sock_and_conn.append(peer)
                        active_conn.append(sock_and_conn)
                        #=====================================
                        message_request = {}
                        message_request["type"] = CHAT_PROTOCOL_CONNECT_ACK
                        message_request["peer_name"] = name
                        message_request["port"] = our_port
                        message_request["ip_peer"] = my_ip_addr
                        message_request["id_peer"] = my_id_peer
                        #=====================================
                        peer.send(send_client_message(message_request))
                        print('{} has connected with you'.format(data["peer_name"]))
                    if data["type"] == CHAT_PROTOCOL_CONNECT_ACK:
                        sock_and_conn = []
                        active_conn.append([data["peer_name"],data["port"],data["ip"],data["id_peer"]])
                        sock_and_conn.append([data["peer_name"],data["port"],data["ip"],data["id_peer"]])
                        sock_and_conn.append(peer)
                        active_conn_sock.append(sock_and_conn)
                        print("connection accepted!!!")
                    if data["type"] == CHAT_PROTOCOL_DIS:
                        #manage incoming disconnection
                        sock_and_conn_aux = []
                        active_conn.remove([data["peer_name"],data["port"],data["ip"],data["id_peer"]])
                        sock_and_conn_aux.append([data["peer_name"],data["port"],data["ip"],data["id_peer"]])
                        sock_and_conn_aux.append(peer)
                        active_conn_sock.remove(sock_and_conn_aux)
                        socket_peer_list.remove(peer)
                         #=====================================
                        message_request = {}
                        message_request["type"] = CHAT_PROTOCOL_DIS_ACK
                        message_request["peer_name"] = name
                        message_request["port"] = our_port
                        message_request["ip_peer"] = my_ip_addr
                        message_request["id_peer"] = my_id_peer
                        #=====================================
                        peer.send(send_client_message(message_request))
                    if data["type"] == CHAT_PROTOCOL_DIS_ACK:
                        sock_and_conn_aux = []
                        active_conn.remove([data["peer_name"],data["port"],data["ip"],data["id_peer"]])
                        sock_and_conn_aux.append([data["peer_name"],data["port"],data["ip"],data["id_peer"]])
                        sock_and_conn_aux.append(peer)
                        active_conn_sock.remove(sock_and_conn_aux)
                        socket_peer_list.remove(peer)
                        peer.close()
                        print('disconnected from: ' + data["peer_name"])
                    if data["type"] == CHAT_PROTOCOL_MSG:
                        print("{}@{} > {}".format(data["peer_name"],name,data["message"]))
                else:
                    #if no data
                    socket_peer_list.remove(peer)
                    peer.close()
                
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
        server_listen.start()
    ours_server_listen = Thread(target= thread_our_server_listen)
    server_read = Thread(target= thread_read)
    server_read.start()
    ours_server_listen.start()
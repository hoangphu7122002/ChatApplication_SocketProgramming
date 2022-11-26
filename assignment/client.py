import socket
from threading import *
from hyper_parameter import *
import pickle
import signal
import sys
from helper_function import *
import time    
import os
    
name = sys.argv[1]
our_port = int(sys.argv[2])
p2p_server_addr = sys.argv[3]
p2p_server_port = int(sys.argv[4])
#to modify later
my_ip_addr = '127.0.0.1'

#thread our_server    
active_conn = []
active_conn_sock = []    
socket_peer_list = []     
    

peer_list = []
my_id_peer = None

#to connect server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((p2p_server_addr,p2p_server_port))

ours_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ours_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
ours_server.bind(('',our_port))
ours_server.listen(QUEUE_CLIENT)

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
    
def thread_read():
    while True:
        global peer_list
        global my_id_peer
        global socket_peer_list
        global active_conn
        msg = input('>:')
        if is_command(msg,'/transfer_file'):
            path_file = msg.split(' ')[2]
            id_peer = msg.split(' ')[1]
            if os.path.exists("{}/{}".format(name,path_file)) == False:
                print("file {} not exist!!".format(path_file))
            try:
                id_peer = int(id_peer)
                if is_already_Connected(active_conn,id_peer):
                    peer_to_send = get_sockpeer_element(active_conn_sock,id_peer)
                    message_request = {}
                    message_request["type"] = CHAT_PROTOCOL_TRANSFER_FILE
                    message_request["peer_name"] = name
                    message_request["port"] = our_port
                    message_request["ip_peer"] = my_ip_addr
                    message_request["id_peer"] = my_id_peer
                    message_request["file_name"] = path_file 
                    data = open("{}/{}".format(name,path_file), 'rb').read()        
                    message_request["data"] = data    
                    peer_to_send.sendall(send_client_message(message_request))
                    print("file {} has been send to: {}".format(path_file,id_peer))
                else:
                    print("id_peer: {} not found...".format(id_peer_to_send))
            except:
                print("invalid id peer")
        if is_command(msg,'/transfer_group'):
            path_file = msg.split(' ')[1]
            if os.path.exists("{}/{}".format(name,path_file)) == False:
                print("file {} not exist!!".format(path_file))
                continue
            message_request = {}
            message_request["type"] = CHAT_PROTOCOL_TRANSFER_GROUP
            message_request["peer_name"] = name
            message_request["port"] = our_port
            message_request["id_peer"] = my_id_peer
            message_request["file_name"] = path_file
            data = open("{}/{}".format(name,path_file), 'rb').read()        
            message_request["data"] = data    
            server.send(send_client_message(message_request))        
        if is_command(msg,'/chat_group'):
            message_request = {}
            message_request["type"] = CHAT_PROTOCOL_CHAT_GROUP
            message_request["peer_name"] = name
            message_request["port"] = our_port
            message_request["id_peer"] = my_id_peer
            message_request["message"] = get_msg_to_send(msg,1)
            server.send(send_client_message(message_request))        
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
            # message_request["id_peer"] = my_id_peer
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
                    print(peer_to_connect)
                    aux_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    aux_peer.connect((peer_to_connect[2],peer_to_connect[1])) #aka: port, hostname
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
                if is_already_Connected(active_conn,id_peer_to_send):
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
                if data["type"] == CHAT_PROTOCOL_CHAT_GROUP_ACK:
                    _name = data["peer_name"]
                    msg = data["message"]
                    print("{}>{}".format(_name,msg))
                if data["type"] == CHAT_PROTOCOL_HI_ACK:
                    global peer_list 
                    global my_id_peer  
                    peer_list = data["peer_list"]
                    my_id_peer = data["id_peer"]
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
                if data["type"] == CHAT_PROTOCOL_TRANSFER_GROUP_ACK:
                    peer_name = data["peer_name"]
                    data_file = data["data"]
                    file_name = data["file_name"]
                    with open("{}/{}".format(name,file_name),'wb') as f:
                        f.write(data_file)
                    print("file {} transfer success from {} to {}!!".format(file_name,peer_name,name))
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
        conn, _ = ours_server.accept()
        socket_peer_list.append(conn)

def thread_our_server_handle():
    while True:
        global socket_peer_list
        for peer in socket_peer_list:
            global active_conn
            global active_conn_sock
            if (peer != server) and (peer != ours_server):
                data = get_client_data(peer)
                if data:
                    if data["type"] == CHAT_PROTOCOL_CONNECT:
                        sock_and_conn = []
                        active_conn.append([data["peer_name"],data["port"],data["ip_peer"],data["id_peer"]])
                        sock_and_conn.append([data["peer_name"],data["port"],data["ip_peer"],data["id_peer"]])
                        sock_and_conn.append(peer)
                        active_conn_sock.append(sock_and_conn)
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
                        active_conn.append([data["peer_name"],data["port"],data["ip_peer"],data["id_peer"]])
                        sock_and_conn.append([data["peer_name"],data["port"],data["ip_peer"],data["id_peer"]])
                        sock_and_conn.append(peer)
                        active_conn_sock.append(sock_and_conn)
                        print("connection accepted!!!")
                    if data["type"] == CHAT_PROTOCOL_DIS:
                        #manage incoming disconnection
                        sock_and_conn_aux = []
                        active_conn.remove([data["peer_name"],data["port"],data["ip_peer"],data["id_peer"]])
                        sock_and_conn_aux.append([data["peer_name"],data["port"],data["ip_peer"],data["id_peer"]])
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
                        active_conn.remove([data["peer_name"],data["port"],data["ip_peer"],data["id_peer"]])
                        sock_and_conn_aux.append([data["peer_name"],data["port"],data["ip_peer"],data["id_peer"]])
                        sock_and_conn_aux.append(peer)
                        active_conn_sock.remove(sock_and_conn_aux)
                        socket_peer_list.remove(peer)
                        peer.close()
                        print('disconnected from: ' + data["peer_name"])
                    if data["type"] == CHAT_PROTOCOL_MSG:
                        print("{}@{} > {}".format(data["peer_name"],name,data["message"]))
                    if data["type"] == CHAT_PROTOCOL_TRANSFER_FILE:
                        peer_name = data["peer_name"]
                        file_name = data["file_name"]
                        file_data = data["data"]
                        with open("{}/{}".format(name,file_name),'wb') as f:
                            f.write(file_data)
                        print("file {} transfer success from {}!!".format(file_name,peer_name))
                else:
                    #if no data
                    socket_peer_list.remove(peer)
                    peer.close()
                
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print('Error: usage: ./' + sys.argv[0] + ' <username> <your_listen_port> <IP_P2P_server> <Port>')
        sys.exit(0)
    if connect_server():
        message_first = {}
        message_first["type"] = CHAT_PROTOCOL_HI
        message_first["peer_name"] = name
        message_first["port"] = our_port
        
        server.send(send_client_message(message_first))
        server_listen = Thread(target= thread_server_listen)
        server_listen.start()
    ours_server_listen = Thread(target= thread_our_server_listen)
    ours_server_handle = Thread(target=thread_our_server_handle)
    server_read = Thread(target= thread_read)
    server_read.start()
    ours_server_listen.start()
    ours_server_handle.start()
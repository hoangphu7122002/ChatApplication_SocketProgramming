import pickle
HEADER_LENGTH = 10

def print_help(name):
    print('Hi '+name+' !\n\n')
    print('These are the commands that you can use:\n')
    print('\t/help\t\tTo consult the commands and guides for using the chat')
    print('\t/quit\t\tTo exit, it close all connections')
    print('\t/update\t\tTo update your peer list')
    print('\t/show_peers\tTo show your peers table')
    print('\t/show_connection\tTo show your current active connections')
    print('\t/connection [id]\tTo connect with your peers')
    print('\t/dis_connection [id]\tTo disconnect with your peers')
    print('\t/msg\t\tTo send a msg to some connected peer')
    print('\t\t\tUsage: /msg [id] messsage\n\n\t\t\tExample: /msg 1 Hi everyone! :)')     
    
    input("Press Enter to continue...")
    
def print_peer_table(name, peer_list):
    print('Hi '+name+' !\n\n')
    print('\t\t-- Peer table --\n')
    for peer in peer_list:
        print('+ Name: '+peer[0]+'\t | Port: '+str(peer[1])+' | Ip: '+peer[2]+' | Id_peer: '+str(peer[3]))
    input("\n\n\nPress Enter to continue...")
    
def print_conn_table(name, active_conn):
    print('Hi '+name+' !\n\n')
    print('\t\t-- Active connections table --\n')
    print(active_conn)
    for peer in active_conn:
        print('+ Name: '+peer[0]+'\t | Port: '+str(peer[1])+' | Ip: '+peer[2]+' | Id_peer: '+str(peer[3]))
    input("\n\n\nPress Enter to continue...")
    
def get_peer_element(peer_list, my_peer_id):
    for peer in peer_list:
        if peer[3] == my_peer_id:
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
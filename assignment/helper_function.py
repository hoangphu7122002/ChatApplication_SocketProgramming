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
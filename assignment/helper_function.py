def print_help(name):
    print('Hi '+name+' !\n\n')
    print('These are the commands that you can use:\n')
    print('\t/help\t\tTo consult the commands and guides for using the chat')
    print('\t/quit\t\tTo exit, it close all connections')
    print('\t/timeup\t\tTo get the time you have connected in the chat')
    print('\t/stats\t\tTo get statistics about your activity in the chat')
    print('\t/update\t\tTo update your peer list')
    print('\t/show_peers\tTo show your peers table')
    print('\t/showconn\tTo show your current active connections')
    print('\t/conn [id]\tTo connect with your peers')
    print('\t/dis  [id]\tTo disconnect with your peers')
    print('\t/msg\t\tTo send a msg to some connected peer')
    print('\t\t\tUsage: /msg [id] @messsage\n\n\t\t\tExample: /msg 1 @Hi everyone! :)')     
    
    input("Press Enter to continue...")
    
def print_peer_table(name, peer_list):
    print('Hi '+name+' !\n\n')
    print('\t\t-- Peer table --\n')
    for peer in peer_list:
        print(peer[0],type(peer[0]))
        print(peer[1],type(peer[1]))
        print(peer[2],type(peer[2]))
        print(peer[3],type(peer[3]))
        print('+ Name: '+peer[0]+'\t | Port: '+str(peer[1])+' | Ip: '+peer[2]+' | Id_peer: '+str(peer[3]))
    input("\n\n\nPress Enter to continue...")
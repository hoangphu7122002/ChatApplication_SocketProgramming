from tkinter import *
from tkinter import font
from tkinter import ttk
from helper_function import *
from hyper_parameter import *
from threading import *
import socket
import sys

# server ip
p2p_server_addr = socket.gethostname(socket.gethostbyname())
p2p_server_port = 1234

name = ""
our_port = 1234

# to connect server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((p2p_server_addr, p2p_server_port))

ours_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ours_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def connect_server(name, pwd):
    message = {}
    message["user_name"] = name
    message["password"] = pwd
    message["type"] = AUTHENTICATION
    server.send(send_client_message(message))

    print("wait to connect server")
    data_auth = get_client_data(server)
    if data_auth["user_name"] != "SERVER" or data_auth["type"] != AUTH_PROTOCOL_SUCCESS:
        print("close connection!!!")
        server.close()
        return False
    return True


def thread_server_listen():
    while True:
        try:
            data = get_client_data(server)
            if data:
                if data["type"] == CHAT_PROTOCOL_CHAT_GROUP_ACK:
                    _name = data["peer_name"]
                    msg = data["message"]
                    print("{}>{}".format(_name, msg))
                if data["type"] == CHAT_PROTOCOL_HI_ACK:
                    global peer_list
                    global my_id_peer
                    peer_list = data["peer_list"]
                    my_id_peer = data["id_peer"]
                    print('Server:> the list of peers was received correctly, ' +
                          str(len(peer_list))+' total active peers')
                if data["type"] == CHAT_PROTOCOL_BYE_ACK:
                    server.close()
                    print("Server:> Closing connections with server.......")
                    print('\n\nGoodbye '+name+'!\n')
                    input("Press Enter to continue...")
                    sys.exit(0)
                if data["type"] == CHAT_PROTOCOL_UPDATE_ACK:
                    peer_list = data["peer_list"]
                    print('Server:> the list of peers was received correctly, ' +
                          str(len(peer_list))+' total active peers')
                if data["type"] == CHAT_PROTOCOL_TRANSFER_GROUP_ACK:
                    peer_name = data["peer_name"]
                    data_file = data["data"]
                    file_name = data["file_name"]
                    with open("{}/{}".format(name, file_name), 'wb') as f:
                        f.write(data_file)
                    print("file {} transfer success from {} to {}!!".format(
                        file_name, peer_name, name))
            else:
                server.close()
                print("Goodbye!!!")
                break
        except:
            server.close()
            print("Goodbye!!!")
            break


class GUI:
    def __init__(self):
        # Name and Port in server
        self.ports = [("HP7122002", 6000), ("GP2002", 6001),
                      ("dakLoc", 6002), ("nguyen", 6003)]

        # Create Window
        self.Window = Tk()
        self.Window.withdraw()

        # Create the Login window
        self.login = Toplevel()

        # Login title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400, height=300)

        # Label: Please login to continue
        self.pls = Label(self.login,
                         text="Please login to continue",
                         justify=CENTER,
                         font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        # Label: Name
        self.labelName = Label(self.login, text="Name: ", font="Helvetica 12")
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

        # Entry box: Name
        self.entryName = Entry(self.login, font="Helvetica 14")
        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        # Label: Password
        self.labelPass = Label(
            self.login, text="Password: ", font="Helvetica 12")
        self.labelPass.place(relheight=0.2, relx=0.1, rely=0.4)

        # Entry box: Password
        self.entryPass = Entry(self.login, font="Helvetica 14")
        self.entryPass.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.4)

        # Button: Sign in
        # Send data to server
        self.go = Button(self.login,
                         text="SIGN IN",
                         font="Helvetica 14 bold",
                         command=lambda: goAhead(self.entryName.get(), self.entryPass.get()))
        self.go.place(relx=0.4,
                      rely=0.55)

        # GoAhead funcion:
        # Bind our server with our port
        # Start to listen
        # Connect to main server
        # Remember to import helper file in project
        def goAhead(name, pwd):
            flag = False
            for port in self.ports:
                if (port[0] == name):
                    our_port = port[1]
                    break
            print (our_port)
            ours_server.bind('', our_port)
            ours_server.listen(5)

            if connect_server(name, pwd):
                message_first = {}
                message_first["type"] = CHAT_PROTOCOL_HI
                message_first["peer_name"] = name
                message_first["port"] = our_port

                server.send(send_client_message(message_first))
                server_listen = Thread(target=thread_server_listen)

            return

        self.Window.mainloop()


g = GUI()

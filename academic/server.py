import socket
import time
import pickle

HEADER_SIZE = 10

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),1234))
s.listen(5)

while True:
    client_socket, address = s.accept()
    print(f"Connection from {address} has been established!")
    # msg = 'Welcome to server!'
    # msg = f'{len(msg):<{HEADER_SIZE}}' + msg
    # client_socket.send(bytes(msg,"utf-8"))
    
    # while True:
    #     time.sleep(3)
    #     msg = f"the time is {time.time()}"
    #     msg = f'{len(msg):<{HEADER_SIZE}}' + msg
    #     client_socket.send(bytes(msg,"utf-8"))
    d = {1 : "Hey", 2 : "Hello"}
    msg = pickle.dumps(d)
    msg = bytes(f'{len(msg):<{HEADER_SIZE}}',"utf-8") + msg
    client_socket.send(msg)
    
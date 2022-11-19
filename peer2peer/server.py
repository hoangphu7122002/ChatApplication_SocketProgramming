import socket
import sys
import time

s = socket.socket()
host = socket.gethostname()
print("server will start on host:",host)
port = 1234
s.bind((host,port))

print("Server is active!!!")

s.listen(1)
conn,add = s.accept()
print(add,"has connected")

while True:
    message = input(str("Server:>>"))
    message = message.encode()
    conn.send(message)
    incomming_message = conn.recv(1024)
    incomming_message = incomming_message.decode()
    print("My:>>",incomming_message)
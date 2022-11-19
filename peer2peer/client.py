import socket
import sys
import time

s = socket.socket()
host = input(str("please enter host name:"))

port = 1234
s.connect((host,port))
print("connected to server")
while True:
    incoming_message = s.recv(1024)
    incoming_message = incoming_message.decode()
    print("Server:>>",incoming_message)
    message = input(str("Client:>>"))
    message = message.encode()
    s.send(message)
import socket

HOST = 'localhost'  # The server's hostname or IP address
PORT = 8080         # The port used by the server

filename = 'transactions.txt'  # Replace with your file name
num_elements = 1000000  # Number of elements you want to read

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

message = '3'
s.sendall(message.encode('utf-8'))
data = s.recv(1024)

message = 'D000000000000000000000000000000000000000000000000D000000000000000000000000000000000000000000000000'
s.sendall(message.encode('utf-8'))
data = s.recv(1024)

message = 'A000000000000000000000000000000000000000000000000'
s.sendall(message.encode('utf-8'))
data = s.recv(1024)

message = 'G000000000000000000000000000000000000000000000000G000000000000000000000000000000000000000000000000'
s.sendall(message.encode('utf-8'))
data = s.recv(1024)

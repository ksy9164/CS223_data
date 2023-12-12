import socket

HOST = 'localhost'  # The server's hostname or IP address
PORT = 8080         # The port used by the server

filename = 'transactions.txt'  # Replace with your file name
num_elements = 1000000  # Number of elements you want to read

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.sendall(num_elements.encode())
with open(filename, 'r') as file:
    for _ in range(num_elements):
        line = file.readline()
        message = line
        s.sendall(message.encode())
        data = s.recv(1024)

s.close()




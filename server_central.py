import socket
from queue import Queue
rows = 4
cols = 65536

table = [[0 for _ in range(cols)] for _ in range(rows)]

table_name = ["User Table", "Product Table", "Order Table", "Review Table"]

transasction_values = [0, 0, 0, 5, 11, 5, 13]
waitQ = Queue()

def calculate_binary_value(value):
    char_to_value = {'A': 64, 'B': 32, 'C': 16, 'D': 8, 'E': 4, 'F': 2, 'G': 1}

    total_value = 0
    total_value += char_to_value.get(value, 0)  # Add the value, 0 if char not found

    return total_value

result = calculate_binary_value("ABCG")
print(result)  # This will output 97 for "ABCG" (64 + 32 + 1 + 1)


def check_transaction(trans_char):
    if trans_char == 'A':
        return 0
    elif trans_char == 'B' or trans_char == 'C':
        return 1
    elif trans_char == 'D' or trans_char == 'F' or trans_char == 'G':
        return 2
    elif trans_char == 'E':
        return 0

def check_multi(trans_char):
    if trans_char == 'D' or trans_char == 'F' or trans_char == 'G'or trans_char == 'E' :
        return True
    else : 
        return False


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = ''  # Symbolic name meaning all available interfaces

EAST_PORT = 8080
CENTER_PORT = 8085
WEST_PORT = 8082

s.bind((HOST, CENTER_PORT))
s.listen()

print("Server is listening on port {PORT}")

sch_val = 0
time_max = 0
time_cur = 0


while True:
    # Accept a connection
    conn, addr = s.accept()
    print("Connected by {addr}")


    # Read and echo back data from the client
    while True:
        data = conn.recv(1024)
        message = data.decode('utf-8')
        trans_order = list(message)
        table_id = check_transaction(trans_order[0])
        message = data.decode('utf-8')
        print(message)
        trans_order = list(message)
        table_id = check_transaction(trans_order[0])
            
        r_idx = ''.join(trans_order[1:17])
        w_idx = ''.join(trans_order[17:33])
        w_val = ''.join(trans_order[33:49])
        r_data = table[table_id][int(r_idx) % 65536]
        if w_idx != 0:
            table[table_id][int(w_idx)] = int(w_val)

        conn.sendall(data)

    # Close the connection
    conn.close()


import socket
from queue import Queue
rows = 4
cols = 65536

table = [[1 for _ in range(cols)] for _ in range(rows)]

table_name = ["User Table", "Product Table", "Order Table", "Review Table"]

transasction_values = [0, 0, 0, 5, 11, 5, 13]
waitQ = Queue()

def calculate_binary_value(value):
    char_to_value = {'A': 64, 'B': 32, 'C': 16, 'D': 8, 'E': 4, 'F': 2, 'G': 1}

    total_value = 0
    total_value += char_to_value.get(value, 0)  # Add the value, 0 if char not found

    return total_value

def check_transaction(trans_char):
    if trans_char == 'A':
        return 0
    elif trans_char == 'B' or trans_char == 'C':
        return 1
    elif trans_char == 'D' or trans_char == 'F' or trans_char == 'G':
        return 2
    else:
        return 0

def check_multi(trans_char):
    if trans_char == 'D' or trans_char == 'F' or trans_char == 'G'or trans_char == 'E' :
        return True
    else : 
        return False


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 8080  # Port to listen on (non-privileged ports are > 1023)

CENTER_PORT = 8085
WEST_PORT = 8082

s.bind((HOST, PORT))
s.listen()

print("Server is listening on port {PORT}")

sch_val = 0
time_max = 0
time_cur = 0


ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.connect(('localhost', CENTER_PORT))
ss.settimeout(1) 

cnt = 0
while True:
    # Accept a connection
    conn, addr = s.accept()
    print("Connected by {addr}")

    data = conn.recv(1024)
    message = data.decode('utf-8')
    t_num = int(message)
    print("Total" , t_num, "new request has been recieved")
    conn.sendall(data)

    # Read and echo back data from the client
    while cnt < t_num:
        try:
            data_from_center = ss.recv(1024)
            m_center = data_from_center.decode('utf-8')
            print("Got response for transaction ", m_center[0])
            bitmap = list(m_center)
            if data:
                sch_val = sch_val & bitmap
            # check queue
            if bitmap == waitQ[0]:
                msg_t = waitQ.get()
                trans_order_t = list(message)
                table_id_t = check_transaction(trans_order_t[0])
                print("Transaction processing start ", trans_order_t[0]);
                r_idx_t = ''.join(trans_order_t[1:17])
                w_idx_t = ''.join(trans_order_t[17:33])
                w_val_t = ''.join(trans_order_t[33:49])
                r_data_t = table[table_id_t][int(r_idx_t)]
                if w_idx_t != 0:
                    table[table_id_t][int(w_idx_t)] = int(w_val_t)
            if check_multi(trans_order_t[0]) or (table_id_t == 1):
                sch_val = sch_val | calculate_binary_value(trans_order_t[0])
                msg = ''.join(trans_order_t[49:98])
                msg = msg + str(r_data_t)
                print("Request to Central Server for remaining transaction")
                ss.sendall(msg.encode('utf-8'))
                time_max = time_max + 80
            else:
                if time_cur + 4 <= time_max:
                    time_cur = time_cur + 4
                else :
                    time_cur = time_cur + 4
                    time_max = time_max + 4

            time_cur = time_cur + 80
        except :
            print("")

        data = conn.recv(1024)
        message = data.decode('utf-8')
        print(message)
        trans_order = list(message)
        table_id = check_transaction(trans_order[0])
        print("Transaction processing start ", cnt , " " , trans_order[0]);

        r_idx = 0 
        w_idx = 0 
        w_val = 0 
        r_data = 0

        if (int(sch_val) & int(table_id)) == 0:
            if table_id != 1:
                r_idx = ''.join(trans_order[1:17])
                w_idx = ''.join(trans_order[17:33])
                w_val = ''.join(trans_order[33:49])
                r_data = table[table_id][int(r_idx) % 65536]
                if w_idx != 0:
                    table[table_id][int(w_idx)] = int(w_val)
        else :
            waitQ.put(message)
            continue

        if check_multi(trans_order[0]) or (table_id == 1):
            if check_multi(trans_order[0]):
                sch_val = sch_val | calculate_binary_value(trans_order[0])
                msg = ''.join(trans_order[49:98])
                msg = msg + str(r_data)
                print("Request to Central Server for remaining transaction")
                ss.sendall(msg.encode('utf-8'))
                time_max = time_max + 80
            else:
                msg = ''.join(trans_order[0:49])
                msg = msg + str(r_data)
                print("Request to Central Server for remaining transaction")
                ss.sendall(msg.encode('utf-8'))
                time_max = time_max + 80

        else:
            if time_cur + 4 <= time_max:
                time_cur = time_cur + 4
            else :
                time_cur = time_cur + 4
                time_max = time_max + 4


        conn.sendall(data)
        cnt = cnt + 1
        print("Total Elapsed TIme is ", time_max)

    # Close the connection
    conn.close()


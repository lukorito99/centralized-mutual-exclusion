import socket
import threading

port = 1250
header = 64

# server = '192.168.175.1'
s = socket.gethostbyname(socket.gethostname())
ADDR = (s, port)

disconnect_message = 'DISCONNECTING!'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind(ADDR)
except socket.error as e:
    print(str(e))


processes=dict()
critical_region=[49,121,169,289]
queued=list()
m=['Request','Ok','Release']

processes['A']=queued

def client_handler(conn, addr):
    print(f'{addr} connected.\n')
    connected = True

    r_status=' '
    while connected:

        message_length = conn.recv(header).decode('utf-8')

        if message_length:
            l = int(message_length)
            message = conn.recv(l).decode('utf-8')
            if message == disconnect_message:
                connected = False
            else:

                if message == m[0]:
                    if r_status == ' ':
                       r_status='in_use'
                       processes['A'].append(conn)
                       conn.sendall(m[1].encode('utf-8'))

                    else:
                       r_status='in_use'
                       processes['A'].append(conn)
                       #sendall(m[1].encode('utf-8'))

                if message == m[2]:
                    processes['A'].remove(conn)
                    print(message)
                    r_status=' '

                connected = False


def start():
    server.listen()

    print('Server is listening on:', s)

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=client_handler, args=(conn, addr))

        thread.start()
        print(f'[ACTIVE CONNECTIONS:]  {threading.activeCount() - 1}')


print('server is starting...\n')
start()

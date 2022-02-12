import socket
import threading

port = 1250
header = 64

#server = '192.168.175.1'
s = socket.gethostbyname(socket.gethostname())
addr = (s, port)

disconnect_message = 'DISCONNECTING!'

critical_region=[49,121,169,289]
processes=dict()

n = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(3)]
q=list()

processes[0]=n[0]
processes[1]=n[1]
processes[2]=n[2]


m=['Request','Ok','Release']


def inform(msg,z):

    message=msg.encode('utf-8')

    msg_len = len(message)
    send_len=str(msg_len).encode('utf-8')

    send_len += b' ' * (header - len(send_len))

    processes[z].sendall(send_len)
    processes[z].sendall(message)


def node_sending(f,y):
    processes[f]=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    processes[f].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
       processes[f].connect(addr)

       inform(y,f)

    except socket.error as e:
         pass

def node_recv(h):

    x=processes[h].recv(4096).decode('utf-8')

    if  x == m[1]:
       q=critical_region
       print('Accessing critical region:',*q,'\n')

    inform(disconnect_message,h)
    processes[h].close()



def check():
    if q == critical_region:
       node_sending(0,m[2])
    else:
        print('Critical region',*critical_region,'is being accesed by another process.\n')

node_sending(0,m[0])
check()
node_recv(0)

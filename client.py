from distutils.log import error
import socket
import threading
import sys


SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = SERVER, PORT
FORMAT = 'utf-8'
BUFFERSIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def clean_exit():
    client.send("exit()".encode())
    client.close()
    sys.exit(0)

def receive_msg():
    try:
        while True:
            recv_message = client.recv(BUFFERSIZE)
            if recv_message:
                print(recv_message.decode())
    except OSError:
        print(error)

def send_msg():
    try:
        while True:
            msg = input("")
            if msg != "exit()":
                client.send(msg.encode())
            else:
                clean_exit()
    except EOFError:
        print(error)


threading.Thread(target=receive_msg).start()
send_msg()



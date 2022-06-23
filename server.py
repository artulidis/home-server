from http import client
import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = SERVER, PORT
FORMAT = 'utf-8'
BUFFERSIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}

def get_clients():
    cli_count = 0
    cli_list = []
    for k, v in clients.items():
        if v != 'Anonymous':
            cli_count += 1
            cli_list.append(v)
    print(clients)
    return cli_count, cli_list

def unicast(cli, msg):
    referred_client, referred_message = msg.split(' ', 1)
    referred_client = referred_client.strip('@')
    for k, v in clients.items():
        if v == referred_client:
            k.send(f"{clients[cli]} -> {v}: {referred_message}".encode())
        else:
            k.send(f" ".encode())

def broadcast(cli, msg):
    for c in clients:
            if c != cli:
                c.send(f"{clients[cli]}: {msg}".encode())

    
def handleClient(client):
    clients[client] = 'Anonymous'
    welcome_msg = f"welcome {clients[client]}!\nType name() <username> to change your name\nType online() to check online users\nAdd an @<username> to send direct message\nexit() to exit"
    client.send(welcome_msg.encode())

    while True:
        recv_message = client.recv(BUFFERSIZE).decode()
        if 'name()' in recv_message:
            new_name = recv_message.replace("name() ", "")
            clients[client] = new_name
            print(f"{clients[client]}")
        elif 'online()' in recv_message:
            client_count, client_list = get_clients()
            msg = f"{client_count} registered users are online:\n{', '.join(client_list)}"
            client.send(msg.encode())
        elif '@' in recv_message:
            unicast(client, recv_message)
        elif 'exit()' in recv_message:
            broadcast(client, f"{clients[client]} is leaving the chat...")
            client.close()
            del clients[client]
        else:
            broadcast(client, recv_message)
            


            



def startServer():
    server.listen()
    while True:
        client, addr = server.accept()
        print(f"[SERVER]: {addr} has joined")
        threading.Thread(target=handleClient, args=(client,)).start()


startServer()
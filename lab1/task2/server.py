import socket
import threading

HOST = "127.0.0.1"
PORT = 3000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except Exception as e:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            broadcast(f"{nicknames[index]} left the chat".encode("ascii"))
            nicknames.remove(nicknames[index])
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat".encode("ascii"))
        client.send("Connected to the server!".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()
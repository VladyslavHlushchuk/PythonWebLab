import socket
from datetime import datetime
import time

def printMessage(message: bytes):
    print("---[Message is received]---")
    print(f"[Message] - {message.decode()}")
    print(f"[Time] - {datetime.now()}")
    print("---------------------------")

def wait(seconds=5):
    print(f"[Waiting for {seconds} seconds...]")
    time.sleep(seconds)

def sendMessage(message: bytes, connection: socket):
    print("[Sending the message back]")
    if len(message) != connection.send(message):
        print("[Not the whole message was sent!!!]")
    else:
        print("[The message was sent successfully!!!]")

HOST = "127.0.0.1"
PORT = 4000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

print("[Listening...]")

connection, client_address = server_socket.accept()
print(f"[Accepted from {connection}, {client_address}]")

while True:
    print("\n----------------------------\n")
    message = connection.recv(1024)
    if not message:
        print("[Receive error] - message is empty!")
        continue

    printMessage(message)
    wait(5)
    sendMessage(message, connection)
    print("\n----------------------------\n")

    if message.decode().upper() == "CLOSE":
        break

connection.close()

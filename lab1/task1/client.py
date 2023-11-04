import socket

HOST = "127.0.0.1"
PORT = 4000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

while True:
    print("\n----------------------------\n")
    message = input("Input your message ('CLOSE' to exit) >>> ")

    client_socket.send(message.encode())
    print("The message was sent")

    if message.upper() == "CLOSE":
        break

    echo_message = client_socket.recv(1024)

    print(f"[Echo message] - {echo_message.decode()}")
    print("\n----------------------------\n")

client_socket.close()

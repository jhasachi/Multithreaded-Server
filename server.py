"""

Sachin Kumar Jha
Multithread Server
BIE- PA1

"""

import os
import socket
import msg


def calculate_hash():
    server_data = client_socket.recv(1024).decode()
    server_data = (server_data[:-2])

    n = list()
    for x in server_data:
        n.append(ord(x))

    value = 0
    for num in n:
        value = value + num

    hash_value = (value * 1000) % 65536

    client_socket.sendall(msg.SERVER_KEY_REQUEST.encode())
    key_data = client_socket.recv(1024).decode()

    key_data = int(key_data[:-2])
    server_values = {0: 23019, 1: 32037, 2: 18789, 3: 16443, 4: 18189}
    server_hash = (server_values[key_data] + hash_value) % 65536

    client_socket.sendall(str(str(server_hash) + '\a\b').encode())
    server_confirmation = client_socket.recv(1024).decode()
    server_confirmation = int(server_confirmation[:-2])

    clients_values = {0: 32037, 1: 29295, 2: 13603, 3: 29533, 4: 21952}
    client_hash = (clients_values[key_data] + hash_value) % 65536

    if server_confirmation == client_hash:
        client_socket.sendall(msg.SERVER_OK.encode())
    else:
        client_socket.sendall(msg.SERVER_LOGIN_FAILED.encode())
        client_socket.close()

    print("Authentication Complete")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket creation: ip/tcp
server_socket.bind(('localhost', 65432))  # binding the socket to this device, port number 6666
server_socket.listen(10)  # number of clients

while True:

    client_socket, client_address = server_socket.accept()
    calculate_hash()

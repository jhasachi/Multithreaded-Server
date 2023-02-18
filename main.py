
import socket
from robo import calculate_hash

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(10)

    while True:

        try:
            client_socket, client_address = server_socket.accept()
            calculate_hash(client_socket)
            print(client_address)
            client_socket.settimeout(10)

        except Exception:
            client_socket.close()


if __name__ == '__main__':
    main()
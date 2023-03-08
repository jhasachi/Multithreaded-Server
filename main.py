
import socket
from robo import build_connection

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(10)

    while True:

        try:
            store_message = ''
            client_socket, client_address = server_socket.accept()
            build_connection(client_socket, store_message)
            client_socket.settimeout(1)

        except Exception:
            client_socket.close()

if __name__ == '__main__':
    main()
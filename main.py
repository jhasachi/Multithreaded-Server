"""
Sachin Kumar Jha
TCP Server
BIE-PSI
"""

import socket
from robo import build_connection

def main():
    # socket.AF_INET, specifies that this is an IPv4 socket.
    # socket.SOCK_STREAM, specifies that this is a TCP socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Binds the socket to the local address localhost and port number 63432.
    server_socket.bind(('localhost', 63432))
    # Sets the socket to listen for incoming connections and 10 server can handle at once.
    server_socket.listen(10)

    while True:
        try:
            store_message = ''
            # server_socket.accept() returns a tuple of two values:
            client_socket, client_address = server_socket.accept()
            # @build_connection function used for making connection first and then help robot to reach origin.
            build_connection(client_socket, store_message)
            client_socket.settimeout(1)
        # Except Exception: is used to catch any exception that occurs during communication with the client.
        except Exception:
            client_socket.close()

if __name__ == '__main__':
    main()
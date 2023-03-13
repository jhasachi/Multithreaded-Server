"""
Sachin Kumar Jha
TCP Server
BIE-PSI
"""

import socket
from robo import build_connection

def main():
    """
    socket.AF_INET, specifies that this is an IPv4 socket.
    socket.SOCK_STREAM, specifies that this is a TCP socket.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Binds the socket to the local address localhost and port number 63432.
    server_socket.bind(('localhost', 63432))
    # Sets the socket to listen for incoming connections and 10 server can handle at once.
    server_socket.listen(10)

    while True:
        try:
            # Initialize the store_message with empty string.
            store_message = ''
            # server_socket.accept() returns a tuple of two values:
            # client_socket:
            # Represents the client's connection to the server. This socket can be used to send and receive data from the client.
            #  client_address:
            # Containing the IP address and port number of the client. This can be used to identify the client and keep track of connections.
            client_socket, client_address = server_socket.accept()
            # @build_connection function used for making connection first and then help robot to reach origin.
            build_connection(client_socket, store_message)
            #  set-timeout() this line sets a timeout of 1 second on the client socket object.
            client_socket.settimeout(1)
        # Except Exception: is used to catch any exception that occurs during communication with the client.
        except Exception:
            # client_socket.close() is called to close the client socket if an exception is raised.
            client_socket.close()

if __name__ == '__main__':
    main()
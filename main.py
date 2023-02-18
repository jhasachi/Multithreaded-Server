import socket
from RobotController import calculate_hash


def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(10)

    while True:

        try:
            print("Hello")
            client_socket, client_address = server_socket.accept()
            calculate_hash(client_socket)
            print(client_address)
            client_socket.settimeout(10)

        except Exception:
            print("Some Error Occured, Closing Connection")
            client_socket.close()


if __name__ == '__main__':
    main()
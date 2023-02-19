
import msg

def find_point(client_socket):

    response = move_forward(client_socket, msg.SERVER_MOVE)
    tokens = response[0:-2].split()
    curr_x, curr_y = int(tokens[1]), int(tokens[2])

    if curr_x == 0 and curr_y == 0:
        reach_origin(client_socket, curr_x, curr_y)

    response = move_forward(client_socket, msg.SERVER_MOVE)
    tokens = response[0:-2].split()
    new_x, new_y = int(tokens[1]), int(tokens[2])

    if new_y == 0 and new_x == 0:
        reach_origin(client_socket, new_x, new_y)

    find_position(client_socket, curr_x, curr_y, new_x, new_y)

def find_position(client_socket, current_x, current_y, new_x, new_y):

    # Handle positions on the horizontal and vertical axis.
    if  current_y == new_y:
        if current_x < new_x:
            # Robot is on the horizontal axis, facing east.
            if current_x >= 0:
                rotate_right(client_socket)
                rotate_right(client_socket)
                reach_origin(client_socket, new_x, new_y)
            elif current_x <= 0:
                reach_origin(client_socket, new_x, new_y)
        elif current_x > new_x:
            # Robot is on the horizontal axis, facing west.
            rotate_right(client_socket)
            rotate_right(client_socket)
            reach_origin(client_socket, new_x, new_y)
    elif current_x == new_x:
        if current_y < new_y:
            # Robot is on the vertical axis, facing north.
            rotate_right(client_socket)
            rotate_right(client_socket)
            reach_origin(client_socket, new_x, new_y)
        elif current_y > new_y:
            # Robot is on the vertical axis, facing south.
            rotate_right(client_socket)
            rotate_right(client_socket)
            reach_origin(client_socket, new_x, new_y)

    # Position for point on one of the four quadrant

def reach_origin(client_socket, x1, y1):

    while x1 != 0 and y1 != 0:
        response = move_forward(client_socket, msg.SERVER_MOVE)
        tokens = response.split()
        x1, y1 = int(tokens[1]), int(tokens[2])

    pick_message(client_socket)

def pick_message(client_socket):
    send_command(client_socket, msg.SERVER_PICK_UP)
    read_response(client_socket)
    send_command(client_socket,msg.SERVER_LOGOUT)
    client_socket.close()

def build_connection(client_socket):

    server_data = read_response(client_socket)[:-2]

    n = list()
    for x in server_data:
        n.append(ord(x))

    value = 0
    for num in n:
        value = value + num

    hash_value = (value * 1000) % 65536

    send_command(client_socket,msg.SERVER_KEY_REQUEST)
    key_data = int(read_response(client_socket)[:-2])

    server_values = {0: 23019, 1: 32037, 2: 18789, 3: 16443, 4: 18189}
    server_hash = (server_values[key_data] + hash_value) % 65536

    send_command(client_socket,f"{server_hash}\a\b")
    server_confirmation = int(read_response(client_socket)[:-2])

    clients_values = {0: 32037, 1: 29295, 2: 13603, 3: 29533, 4: 21952}
    client_hash = (clients_values[key_data] + hash_value) % 65536

    if server_confirmation == client_hash:
        send_command(client_socket, msg.SERVER_OK)
        find_point(client_socket)
    else:
        send_command(client_socket, msg.SERVER_LOGIN_FAILED)
        client_socket.close()

def send_command(client_socket, command):
    client_socket.sendall(command.encode())

def read_response(client_socket):
    return client_socket.recv(1024).decode()

def rotate_right(client_socket):
    send_command(client_socket, msg.SERVER_TURN_RIGHT)
    read_response(client_socket)

def rotate_left(client_socket):
    send_command(client_socket, msg.SERVER_TURN_LEFT)
    read_response(client_socket)

def move_forward(client_socket, command):
    send_command(client_socket, command)
    return read_response(client_socket)
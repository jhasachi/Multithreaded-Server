
import msg

def find_point(client_socket):

    new_x, new_y = -1, -1
    curr_x, curr_y = -1, -1

    for i in range(2):
        response = move_forward(client_socket, msg.SERVER_MOVE)
        tokens = response[0:-2].split()
        x, y = int(tokens[1]), int(tokens[2])

        if i == 0:
            curr_x, curr_y = x, y
            if curr_x == 0 and curr_y == 0:
                reach_origin(client_socket, curr_x, curr_y)

        if i == 1:
            new_x, new_y = x, y
            if new_x == 0 and new_y == 0:
                reach_origin(client_socket, new_x, new_y)

    find_method(new_x, new_y, find_direction(new_x, new_y, curr_x, curr_y), client_socket)

def find_direction(curr_x, curr_y, new_x, new_y):

    direction = -1
    # Assigning the value according to direction: North "1" , South "3" , West "2" , East "4"

    if curr_x > new_x:
        direction = 2
    elif curr_x < new_x:
        direction = 4
    elif curr_y > new_y:
        direction = 3
    elif curr_y < new_y:
        direction = 1
    return direction

def find_method(x, y, direction, client_socket):

    if direction == 1:
        if y >= 0:
            for i in range(2):
                rotate_right(client_socket)
                value = 3
                move_to_abscissa(client_socket, x, y, value)

        elif y < 0:
            value = 1
            move_to_abscissa(client_socket, x, y, value)

    if direction == 2:
        if y >= 0:
            rotate_left(client_socket)
            value = 3
            move_to_abscissa(client_socket, x, y, value)
        elif y < 0:
            rotate_right(client_socket)
            value = 1
            move_to_abscissa(client_socket, x, y, value)

    if direction == 3:
        if y >= 0:
            value = 3
            move_to_abscissa(client_socket, x, y, value)
        elif y < 0:
            for i in range(2):
                rotate_right(client_socket)
                value = 1
                move_to_abscissa(client_socket, x, y, value)
    if direction == 4:
        if y >= 0:
            rotate_right(client_socket)
            value = 3
            move_to_abscissa(client_socket, x, y, value)
        elif y < 0:
            rotate_left(client_socket)
            value = 1
            move_to_abscissa(client_socket, x, y, value)

def move_to_abscissa(client_socket, x, y, direction):

    while y != 0:
        response = move_forward(client_socket, msg.SERVER_MOVE)
        token = response.split()
        x, y = int(token[1]), int(token[2])

    if direction == 3:
            rotate_left(client_socket)
    if direction == 1:
            rotate_right(client_socket)

    move_to_ordinates(client_socket, x, y)

def move_to_ordinates(client_socket, x, y):

    while x != 0:
        response = move_forward(client_socket, msg.SERVER_MOVE)
        token = response.split()
        x, y = int(token[1]), int(token[2])

    reach_origin(client_socket, x, y)

def reach_origin(client_socket, x, y):

    if x == 0 and y == 0:
        pick_message(client_socket)

def pick_message(client_socket):

    send_command(client_socket, msg.SERVER_PICK_UP)
    read_response(client_socket)
    send_command(client_socket,msg.SERVER_LOGOUT)
    client_socket.close()

def build_connection(client_socket):

    hash_value = find_hash(client_socket)

    key_data = read_key(client_socket, msg.SERVER_KEY_REQUEST)

    server_values = {0: 23019, 1: 32037, 2: 18789, 3: 16443, 4: 18189}
    server_hash = (server_values[key_data] + hash_value) % 65536

    server_confirmation = read_confirmation(client_socket, f"{server_hash}\a\b")
    server_confirmation = int(server_confirmation[:-2])

    clients_values = {0: 32037, 1: 29295, 2: 13603, 3: 29533, 4: 21952}
    client_hash = (clients_values[key_data] + hash_value) % 65536

    if server_confirmation == client_hash:
        send_command(client_socket, msg.SERVER_OK)
        find_point(client_socket)
    else:
        send_command(client_socket, msg.SERVER_LOGIN_FAILED)
        client_socket.close()

def find_hash(client_socket):
    server_data = read_username(client_socket)[:-2]

    n = list()
    for x in server_data:
        n.append(ord(x))

    value = 0
    for num in n:
        value = value + num

    hash_value = (value * 1000) % 65536

    return hash_value

def rotate_right(client_socket):
    send_command(client_socket, msg.SERVER_TURN_RIGHT)

    value = read_response(client_socket)
    if len(value) > 12:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return value

def rotate_left(client_socket):
    send_command(client_socket, msg.SERVER_TURN_LEFT)

    value = read_response(client_socket)
    if len(value) > 12:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return value

def move_forward(client_socket, command):
    send_command(client_socket, command)

    value = read_response(client_socket)
    if len(value) > 12:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return value

def read_key(client_socket, command):
    send_command(client_socket, command)

    value = read_response(client_socket)
    if len(value) > 5:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    value = int(value[:-2])
    if value > 4 or value < 0:
        send_command(client_socket, msg.SERVER_KEY_OUT_OF_RANGE_ERROR)
        client_socket.close()

    return value

def read_username(client_socket):

    value = read_response(client_socket)

    if not is_valid_username(value):
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return value

def is_valid_username(message):

    if not message or len(message) > 20 or not message.endswith("\a\b"):
        return False

    return True

def read_confirmation(client_socket, command):
    send_command(client_socket, command)

    value = read_response(client_socket)
    if len(value) > 7:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return value

def send_command(client_socket, command):
    client_socket.sendall(command.encode())

def read_response(client_socket):
    return client_socket.recv(1024).decode()

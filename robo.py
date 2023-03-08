
import msg

def initial_coordinates(client_socket, store_message):

    new_x, new_y = -1, -1
    curr_x, curr_y = -1, -1

    for i in range(2):
        store_message, response = move_forward(client_socket, store_message)
        tokens = response[0:-2].split()
        x, y = int(tokens[1]), int(tokens[2])

        if i == 0:
            curr_x, curr_y = x, y
            if curr_x == 0 and curr_y == 0:
                reach_origin(client_socket, curr_x, curr_y, store_message)
        elif i == 1:
            new_x, new_y = x, y
            if new_x == 0 and new_y == 0:
                reach_origin(client_socket, new_x, new_y, store_message)

    if curr_x == new_x and curr_y == new_y:
        store_message, escape = initial_obstacle(client_socket, store_message)
        escape = escape[0:-2].split()
        new_x, new_y = int(escape[1]), int(escape[2])

    face_towards_abscissa(new_x, new_y, find_direction(curr_x, curr_y, new_x, new_y), client_socket, store_message)

def initial_obstacle(client_socket, store_message):

    rotate_right(client_socket, store_message)
    return move_forward(client_socket, store_message)

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

def face_towards_abscissa(x, y, direction, client_socket, store_message):

    value = -1

    if direction == 1:
        if y >= 0:
            for i in range(2):
                rotate_right(client_socket, store_message)
                value = 3
            move_to_abscissa(client_socket, x, y, value, store_message)
        elif y < 0:
            value = 1
            move_to_abscissa(client_socket, x, y, value, store_message)
    elif direction == 2:
        if y >= 0:
            rotate_left(client_socket, store_message)
            value = 3
            move_to_abscissa(client_socket, x, y, value, store_message)
        elif y < 0:
            rotate_right(client_socket, store_message)
            value = 1
            move_to_abscissa(client_socket, x, y, value,store_message)
    elif direction == 3:
        if y >= 0:
            value = 3
            move_to_abscissa(client_socket, x, y, value, store_message)
        elif y < 0:
            for i in range(2):
                rotate_right(client_socket, store_message)
                value = 1
            move_to_abscissa(client_socket, x, y, value, store_message)
    elif direction == 4:
        if y >= 0:
            rotate_right(client_socket, store_message)
            value = 3
            move_to_abscissa(client_socket, x, y, value, store_message)
        elif y < 0:
            rotate_left(client_socket, store_message)
            value = 1
            move_to_abscissa(client_socket, x, y, value, store_message)

def move_to_abscissa(client_socket, x, y, direction, store_message):

    new_x = x
    new_y = y

    while new_y != 0:

        store_message, response = move_forward(client_socket, store_message)
        tokens = response[0:-2].split()
        curr_x, curr_y = new_x, new_y
        new_x, new_y = int(tokens[1]), int(tokens[2])

        if new_x == curr_x and new_y == curr_y:
            store_message, escape = escape_obstacle(client_socket, store_message)
            escape = escape[0:-2].split()
            new_x, new_y = int(escape[1]), int(escape[2])

            if curr_y > 0:
                if new_y < 0:
                    store_message, response = origin_obstacle(client_socket, new_x, new_y, store_message)
                    tokens = response[0:-2].split()
                    new_x, new_y = int(tokens[1]), int(tokens[2])
                    if direction == 1:
                        direction = 3
                    elif direction == 3:
                        direction = 1
            elif curr_y < 0:
                if new_y > 0:
                    store_message, response = origin_obstacle(client_socket, new_x, new_y, store_message)
                    tokens = response[0:-2].split()
                    new_x, new_y = int(tokens[1]), int(tokens[2])
                    if direction == 1:
                        direction = 3
                    elif direction == 3:
                        direction = 1

    if direction == 3:
        if new_x < 0:
          rotate_left(client_socket, store_message)
        elif new_x > 0:
          rotate_right(client_socket, store_message)

    elif direction == 1:
        if new_x < 0:
          rotate_right(client_socket, store_message)
        elif new_x > 0:
          rotate_left(client_socket, store_message)

    move_to_ordinates(client_socket, new_x, new_y, store_message)

def move_to_ordinates(client_socket, x, y, store_message):

    new_x = x
    new_y = y

    while new_x != 0:
        store_message, response = move_forward(client_socket, store_message)
        tokens = response[0:-2].split()
        curr_x, curr_y = new_x, new_y
        new_x, new_y = int(tokens[1]), int(tokens[2])

        if new_x == curr_x and new_y == curr_y:
            store_message, escape = escape_obstacle(client_socket, store_message)
            escape = escape[0:-2].split()
            new_x, new_y = int(escape[1]), int(escape[2])

    reach_origin(client_socket, new_x, new_y, store_message)

def escape_obstacle(client_socket, store_message):

    rotate_right(client_socket, store_message)
    move_forward(client_socket, store_message)
    rotate_left(client_socket, store_message)
    move_forward(client_socket, store_message)
    move_forward(client_socket, store_message)
    rotate_left(client_socket, store_message)
    move_forward(client_socket, store_message)
    return rotate_right(client_socket, store_message)

def origin_obstacle(client_socket, x, y, store_message):

    rotate_right(client_socket, store_message)
    move_forward(client_socket, store_message)
    rotate_right(client_socket, store_message)
    return move_forward(client_socket, store_message)

def reach_origin(client_socket, x, y, store_message):

    if x == 0 and y == 0:
        pick_message(client_socket, store_message)

def pick_message(client_socket, store_message):

    confirmation_message(client_socket,msg.SERVER_PICK_UP, store_message)
    send_command(client_socket,msg.SERVER_LOGOUT)
    client_socket.close()

def build_connection(client_socket, store_message):
    # This function help's in building the connection between server and client.
    store_message, hash_value = find_hash(client_socket, store_message)
    store_message, key_data = read_key(client_socket, store_message)

    server_values = {0: 23019, 1: 32037, 2: 18789, 3: 16443, 4: 18189}
    # By the help of dictionary we check value for resulting server key.
    server_hash = (server_values[key_data] + hash_value) % 65536

    store_message, server_confirmation = send_confirmation(client_socket, f"{server_hash}\a\b", store_message)
    # From this function we will send confirmation code by adding \a\b in the end and collect server confirmation code.
    server_confirmation = int(server_confirmation[:-2])

    clients_values = {0: 32037, 1: 29295, 2: 13603, 3: 29533, 4: 21952}
    client_hash = (clients_values[key_data] + hash_value) % 65536

    if server_confirmation == client_hash:
        # Here we check calculated confirmation code is similar to server confirmation code.
        send_command(client_socket, msg.SERVER_OK)
        initial_coordinates(client_socket, store_message)
    else:
        send_command(client_socket, msg.SERVER_LOGIN_FAILED)
        client_socket.close()

def find_hash(client_socket, store_message):

    store_message, server_data = read_username(client_socket, store_message)
    server_data = server_data[:-2]

    n = list()
    for x in server_data:
        n.append(ord(x))
        # Using ord function we can access ascii value of given data and store in list by using append function.
    value = 0
    for num in n:
        value = value + num
    hash_value = (value * 1000) % 65536

    return store_message, hash_value

def rotate_right(client_socket, store_message):

    send_command(client_socket, msg.SERVER_TURN_RIGHT)
    store_message, value = get_message(client_socket, store_message)


    if len(value) > 12:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return store_message, value

def rotate_left(client_socket, store_message):

    send_command(client_socket, msg.SERVER_TURN_LEFT)
    store_message, value = get_message(client_socket, store_message)

    if len(value) > 12:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return store_message, value

def move_forward(client_socket, store_message):

    send_command(client_socket, msg.SERVER_MOVE)
    store_message, value = get_message(client_socket, store_message)

    if len(value) > 12:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return store_message, value

def read_key(client_socket, store_message):

    send_command(client_socket, msg.SERVER_KEY_REQUEST)
    store_message, value = get_message(client_socket, store_message)

    try:
        value = int(value.rstrip('\a\b'))
        # rstrip used to remove any occurrences of the escape characters "\a\b" from the end of the value string.
    except ValueError:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    if len(str(value)) > 5:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    if value > 4 or value < 0:
        send_command(client_socket, msg.SERVER_KEY_OUT_OF_RANGE_ERROR)
        client_socket.close()

    return store_message, value

def read_username(client_socket, store_message):
    store_message, value = get_message(client_socket, store_message)

    if not is_valid_username(value):
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return store_message, value

def is_valid_username(message):

    if not message or len(message) > 20 or not message.endswith("\a\b"):
        return False

    return True

def send_confirmation(client_socket, command, store_message):

    send_command(client_socket, command)
    store_message, value = get_message(client_socket, store_message)

    if len(value) > 7:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()
    elif any(char.isspace() for char in value):
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()
    else:
        return store_message, value

def confirmation_message(client_socket, command, store_message):

    send_command(client_socket, command)
    store_message, value = get_message(client_socket, store_message)

    if len(value) > 100:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()
    else:
        return store_message, value

def get_message(client_socket, store_message):

    message_index = store_message.find('\a\b')

    if message_index == -1:

        while True:

            read_data = read_message(client_socket)
            store_message += read_data

            message_index = store_message.find('\a\b')

            if message_index == -1:
                continue
            else:
                correct_message = store_message[:message_index + 2]
                store_message = store_message[message_index + 2:]
                return store_message, correct_message

    correct_message = store_message[:message_index + 2]
    store_message = store_message[message_index + 2:]

    return store_message, correct_message

def send_command(client_socket, command):
    client_socket.sendall(command.encode())

def read_message(client_socket):
    client_socket.settimeout(1)
    return client_socket.recv(1024).decode()

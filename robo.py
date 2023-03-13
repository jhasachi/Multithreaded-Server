
import msg

def initial_coordinates(client_socket, store_message):
    # Initialize the variable value to -1.
    new_x, new_y = -1, -1
    curr_x, curr_y = -1, -1
    # Used for loop for two time movement.
    for i in range(2):
        # @move_forward function used to requesting robot to move forward.
        store_message, response = move_forward(client_socket, store_message)
        # use split function to spilt on the basics of spaces and use slicing for storing coordinates value.
        tokens = response[0:-2].split()
        # x contain x axis value and y contain y axis value.
        x, y = int(tokens[1]), int(tokens[2])
        # use this condition for storing first movement and second movement value differently.
        if i == 0:
            # first movement value stored in curr_x and curr_y.
            curr_x, curr_y = x, y
            # Use this condition to check after the first movement, it's already on the origin.
            if curr_x == 0 and curr_y == 0:
                # @reach_origin function used for helping robot to reach origin.
                reach_origin(client_socket, curr_x, curr_y, store_message)
        elif i == 1:
            # Second movement value stored in new_x and new_y.
            new_x, new_y = x, y
            # Use this condition to check after the second movement, it's already on the origin.
            if new_x == 0 and new_y == 0:
                # @reach_origin function used for helping robot to reach origin.
                reach_origin(client_socket, new_x, new_y, store_message)
    # From this condition we can conclude, there is obstacle in starting position.
    if curr_x == new_x and curr_y == new_y:
        # @initial_obstacle function used for handling from the initial obstacle.
        store_message, escape = initial_obstacle(client_socket, store_message)
        # Use split function to split on the basics of spaces and use slicing to obtain the coordinates.
        escape = escape[0:-2].split()
        # new_x contains the value of x and new_y contains the value of y.
        new_x, new_y = int(escape[1]), int(escape[2])
    # @face_towards_abscissa function use for moving robot and make his toward origin.
    face_towards_abscissa(new_x, new_y, find_direction(curr_x, curr_y, new_x, new_y), client_socket, store_message)

def initial_obstacle(client_socket, store_message):
    # use two simple movement to avoid the initial obstacle.
    rotate_right(client_socket, store_message)
    return move_forward(client_socket, store_message)

def find_direction(curr_x, curr_y, new_x, new_y):

    direction = -1
    # Assigning the value according to direction: North "1" , South "3" , West "2" , East "4"
    # from this logic, obtain direction.
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
    # initialise the variable value to -1.
    value = -1
    # Use different movement pattern for different direction according to logic.
    if direction == 1:
        if y >= 0:
            for i in range(2):
                rotate_right(client_socket, store_message)
                value = 3
            # @move_to_abscissa function used for helping robot to move toward x_axis line.
            move_to_abscissa(client_socket, x, y, value, store_message)
        elif y < 0:
            value = 1
            # @move_to_abscissa function used for helping robot to move toward x_axis line.
            move_to_abscissa(client_socket, x, y, value, store_message)
    elif direction == 2:
        if y >= 0:
            rotate_left(client_socket, store_message)
            value = 3
            # @move_to_abscissa function used for helping robot to move toward x_axis line.
            move_to_abscissa(client_socket, x, y, value, store_message)
        elif y < 0:
            rotate_right(client_socket, store_message)
            value = 1
            # @move_to_abscissa function used for helping robot to move toward x_axis line.
            move_to_abscissa(client_socket, x, y, value,store_message)
    elif direction == 3:
        if y >= 0:
            value = 3
            # @move_to_abscissa function used for helping robot to move toward x_axis line.
            move_to_abscissa(client_socket, x, y, value, store_message)
        elif y < 0:
            for i in range(2):
                rotate_right(client_socket, store_message)
                value = 1
            # @move_to_abscissa function used for helping robot to move toward x_axis line.
            move_to_abscissa(client_socket, x, y, value, store_message)
    elif direction == 4:
        if y >= 0:
            rotate_right(client_socket, store_message)
            value = 3
            # @move_to_abscissa function used for helping robot to move toward x_axis line.
            move_to_abscissa(client_socket, x, y, value, store_message)
        elif y < 0:
            rotate_left(client_socket, store_message)
            value = 1
            # @move_to_abscissa function used for helping robot to move toward x_axis line.
            move_to_abscissa(client_socket, x, y, value, store_message)

def move_to_abscissa(client_socket, x, y, direction, store_message):
    # Initialise new_x and new_y value with function value x and y.
    new_x = x
    new_y = y
    # while loop used for helping the robot to move toward to x_axis line.
    while new_y != 0:
        # @move_forward function used for moving forward.
        store_message, response = move_forward(client_socket, store_message)
        # Use split function to split on the basics spaces and slicing use for storing coordinates value.
        tokens = response[0:-2].split()
        curr_x, curr_y = new_x, new_y
        new_x, new_y = int(tokens[1]), int(tokens[2])
        # Use this condition for handling the obstacle the during the movement.
        if new_x == curr_x and new_y == curr_y:
            store_message, escape = escape_obstacle(client_socket, store_message)
            escape = escape[0:-2].split()
            new_x, new_y = int(escape[1]), int(escape[2])
            # Use this condition to handling the x_axis and y_axis line obstacle.
            if curr_y > 0:
                if new_y < 0:
                    store_message, response = origin_obstacle(client_socket, store_message)
                    tokens = response[0:-2].split()
                    new_x, new_y = int(tokens[1]), int(tokens[2])
                    if direction == 1:
                        direction = 3
                    elif direction == 3:
                        direction = 1
            elif curr_y < 0:
                if new_y > 0:
                    store_message, response = origin_obstacle(client_socket, store_message)
                    tokens = response[0:-2].split()
                    new_x, new_y = int(tokens[1]), int(tokens[2])
                    if direction == 1:
                        direction = 3
                    elif direction == 3:
                        direction = 1
   # Used this condition for after reaching the x_axis perfectly to rotate the robot face toward origin.
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
    # @move_to_ordinates function used for helping robot to reach toward to origin.
    move_to_ordinates(client_socket, new_x, new_y, store_message)

def move_to_ordinates(client_socket, x, y, store_message):
    # Used new_x and new_y to initialise with function value x and y.
    new_x = x
    new_y = y
    # Robot will keep on moving unless until it reach to origin perfectly.
    while new_x != 0:
        store_message, response = move_forward(client_socket, store_message)
        tokens = response[0:-2].split()
        curr_x, curr_y = new_x, new_y
        new_x, new_y = int(tokens[1]), int(tokens[2])
        # Used this condition for handling from obstacle while moving toward origin.
        if new_x == curr_x and new_y == curr_y:
            store_message, escape = escape_obstacle(client_socket, store_message)
            escape = escape[0:-2].split()
            new_x, new_y = int(escape[1]), int(escape[2])
    # @reach_origin used for handling the robot after reaching origin.
    reach_origin(client_socket, new_x, new_y, store_message)

def escape_obstacle(client_socket, store_message):
    # Used combination of movement to avoid obstacle lying around the 2D plane.
    rotate_right(client_socket, store_message)
    move_forward(client_socket, store_message)
    rotate_left(client_socket, store_message)
    move_forward(client_socket, store_message)
    move_forward(client_socket, store_message)
    rotate_left(client_socket, store_message)
    move_forward(client_socket, store_message)
    return rotate_right(client_socket, store_message)

def origin_obstacle(client_socket, store_message):
    # used combination of movement to avoid obstacle while approaching toward x_axis and there is obstacle.
    rotate_right(client_socket, store_message)
    move_forward(client_socket, store_message)
    rotate_right(client_socket, store_message)
    return move_forward(client_socket, store_message)

def reach_origin(client_socket, x, y, store_message):
    # Used this condition to make sure robot finally reach origin or not.
    if x == 0 and y == 0:
        # @pick_message function used for picking the message after reaching the origin.
        pick_message(client_socket, store_message)

def pick_message(client_socket, store_message):
    # @confirmation_message function used for requesting to pick the confirmation message.
    confirmation_message(client_socket,msg.SERVER_PICK_UP, store_message)
    # @send_command function used for sending the message to logout.
    send_command(client_socket,msg.SERVER_LOGOUT)
    # close used to close the connection properly after picking the message.
    client_socket.close()

def build_connection(client_socket, store_message):
    # @find_hash function used for calculating hash value.
    store_message, hash_value = find_hash(client_socket, store_message)
    # @read_key function used for receiving key value.
    store_message, key_data = read_key(client_socket, store_message)
    # By the help of dictionary we check value for resulting server key.
    server_values = {0: 23019, 1: 32037, 2: 18789, 3: 16443, 4: 18189}
    server_hash = (server_values[key_data] + hash_value) % 65536
    # @send_confirmation function send the final calculated value by adding \a\b in the end and collect server confirmation code..
    store_message, server_confirmation = send_confirmation(client_socket, f"{server_hash}\a\b", store_message)
    # removed /a/b from the end by the help of slicing.
    server_confirmation = int(server_confirmation[:-2])

    clients_values = {0: 32037, 1: 29295, 2: 13603, 3: 29533, 4: 21952}
    client_hash = (clients_values[key_data] + hash_value) % 65536

    # Here we check calculated confirmation code is similar to server confirmation code.
    if server_confirmation == client_hash:
        send_command(client_socket, msg.SERVER_OK)
        initial_coordinates(client_socket, store_message)
    else:
        send_command(client_socket, msg.SERVER_LOGIN_FAILED)
        client_socket.close()

def find_hash(client_socket, store_message):
    #used @read_username function for receiving the username.
    store_message, server_data = read_username(client_socket, store_message)
    # with the help of slicing we will remove last two character /a/b
    server_data = server_data[:-2]

    n = list()
    # Using ord function we can access ascii value of given data and store in list by using append function.
    for x in server_data:
        n.append(ord(x))

    value = 0

    for num in n:
        value = value + num

    hash_value = (value * 1000) % 65536

    return store_message, hash_value

def rotate_right(client_socket, store_message):
    # @send_command function send message for to turn right.
    send_command(client_socket, msg.SERVER_TURN_RIGHT)
    # @get_message use for receiving the coordinates and stores information in value.
    store_message, value = get_message(client_socket, store_message)

    # Check whether the length is greater than resulting length.
    if len(value) > 12:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return store_message, value

def rotate_left(client_socket, store_message):
    # @send_command function send message for to turn left.
    send_command(client_socket, msg.SERVER_TURN_LEFT)
    # @get_message use for receiving the coordinates and stores information in value.
    store_message, value = get_message(client_socket, store_message)

    # Check whether the length is greater than resulting length.
    if len(value) > 12:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return store_message, value

def move_forward(client_socket, store_message):
    # @send_command function send message for to move forward and collect the receiving value.
    send_command(client_socket, msg.SERVER_MOVE)
    # @get_message use for receiving the coordinates and stores information in value.
    store_message, value = get_message(client_socket, store_message)
    # Check whether the length is greater than resulting length.
    if len(value) > 12:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return store_message, value

def read_key(client_socket, store_message):
    # @send_command function use for requesting key value.
    send_command(client_socket, msg.SERVER_KEY_REQUEST)
    # @get_message use for receiving the key and stores information in value.
    store_message, value = get_message(client_socket, store_message)

    try:
        # rstrip used to remove any occurrences of the escape characters "\a\b" from the end of the value string.
        value = int(value.rstrip('\a\b'))
    except ValueError:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    # Check whether the length is greater than resulting length.
    if len(str(value)) > 5:
        print(str(len(value)))
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()
    # Check whether the value is greater or smaller than resulting value.
    if value > 4 or value < 0:
        send_command(client_socket, msg.SERVER_KEY_OUT_OF_RANGE_ERROR)
        client_socket.close()

    return store_message, value

def read_username(client_socket, store_message):
    # @get_message use for receiving the username and stores information in value.
    store_message, value = get_message(client_socket, store_message)
    # @in_valid_username checks the correctness of the username.
    if not is_valid_username(value):
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()

    return store_message, value

def is_valid_username(message):
    # check whether message is empty or not, length is greater than the resulting length and ends with /a/b or not.
    if not message or len(message) > 20 or not message.endswith("\a\b"):
        return False

    return True

def send_confirmation(client_socket, command, store_message):
    # @send_command use for requesting the confirmation data.
    send_command(client_socket, command)
    # @get_message use to receive the confirmation data of client.
    store_message, value = get_message(client_socket, store_message)
    # check whether length is greater than the resulting length.
    if len(value) > 7:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()
    # check whether is there any space withing the message.
    elif any(char.isspace() for char in value):
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()
    else:
        return store_message, value

def confirmation_message(client_socket, command, store_message):
    # @send_command use for requesting the final secret message.
    send_command(client_socket, command)
    # @get_message use for receiving the final secret message.
    store_message, value = get_message(client_socket, store_message)
    # check whether length of the message is greater than resulting length.
    if len(value) > 100:
        send_command(client_socket, msg.SERVER_SYNTAX_ERROR)
        client_socket.close()
    else:
        return store_message, value

def get_message(client_socket, store_message):
    # @find use for finding the index value of \a\b and If there's no \a\b then it's return -1.
    message_index = store_message.find('\a\b')

    if message_index == -1:

        while True:
            # @read_message function used for requesting the value.
            read_data = read_message(client_socket)
            store_message += read_data

            message_index = store_message.find('\a\b')

            if message_index == -1:
                continue
            else:
                # @correct_message stores the value from the starting to \a\b.
                correct_message = store_message[:message_index + 2]
                # @store_message store the value from next to \a\b to end.
                store_message = store_message[message_index + 2:]
                return store_message, correct_message
    # @correct_message stores the value from the starting to \a\b.
    correct_message = store_message[:message_index + 2]
    # @store_message store the value from next to \a\b to end.
    store_message = store_message[message_index + 2:]

    return store_message, correct_message

def send_command(client_socket, command):
    """
    :param:
    client_socket this is a socket object that has been created earlier in the code. It represents the client's end of the socket connection.
    :param:
    sendall(): This method of the socket object sends data to the server. Sends all the data until the remote end has received it all.
    :param:
    encode() method is used to convert a string to its corresponding byte representation.
    :return:
    """
    client_socket.sendall(command.encode())

def read_message(client_socket):
    """
    :param:
    set-timeout() this line sets a timeout of 1 second on the client socket object.
    :param:
    recv() this line waits to receive up to 1024 bytes of data from the server and the remaining bytes will be stored on the server's buffer.
    :param:
    decode() this method is used to convert the received bytes to a string and use (UTF-8) for conversion.
    :return:
    """
    client_socket.settimeout(1)
    return client_socket.recv(1024).decode()

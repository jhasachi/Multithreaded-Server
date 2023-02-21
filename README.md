# Client and Server

# Details

The robot should reach that target coordinate and pick the secret message.

Communication between server and robots is implemented via a pure textual protocol.

Each command ends with a pair of special symbols "\a\b".

Server and client both know five pairs of authentication keys.

Username can be any sequence of up to 18 characters.

# Calculating

Calculate "hash" code from the username of the client.

Then adds a server key to the hash.

Resulting confirmation code of server is sent to client.

Client takes the received code and calculates hash.

Then compares it with the expected hash value, which he has calculated from the username.

# Movement

Robot can move only straight, left and right.

After each move command robot sends confirmation.

At the beginning of communication robot position is not known to server.

Server must find out robot position and orientation.

Each robot has a limited number of movements.

The number of turns is not limited.

# Obstacle's

There is several obstacle’s on the way to the target coordinate.

The obstacle spans only a single pair of coordinates.

All neighboring coordinates around the obstacle are always free, therefore the obstacle can be always bypassed.

The obstacle is never placed on the target coordinates [0,0].

If the robot crushes an obstacle (any obstacle) more than 20 times, it broke down and ends the connection.

If the robot doesn’t move, the number of remaining moves is not decreased, but the number of remaining crashes is decreased by one.

# Message

After the robot reaches the target coordinate [0,0].

It attempts to pick up the secret message.

After the robot picks the secret message, it sends to the server.

The server has to answer with logout.

# Bugs

- [x]  Ideal Situation
- [x]  Wrong Confirmation
- [x]  Key out of range
- [x]  Strange username
- [ ]  Segmentation
- [ ]  Merging
- [ ]  Segmentation + Merging
- [ ]  Client Confirmation
- [x]  Unfinished Message
- [x]  Constant Obstacles 1
- [x]  Constant Obstacles 2
- [x]  Constant Obstacles 3
- [ ]  Random Obstacle
- [x]  Max length of username
- [x]  Key is not the number
- [ ]  Space after confirmation
- [x]  Six digit confirmation
- [ ]  Floating point coordinates
- [ ]  Unexpected Spaces
- [x]  Max length of username exceeded
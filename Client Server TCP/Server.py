import socket
import threading

# Identify the Port number for the socket conncetion and the Server IP
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 64  # Number of byte first reseved by the Server
ADDR = (SERVER, PORT)  # define the ADDR for the Socket Connection
FORMAT = "utf-8"  # format of the encription
DISCONNECT_MESSAGE = "!DISCONNECT"
# Define the socket itself by config the family of the socket which is defualt AF_INET which means internet network socket connection and the data Streaming
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now we bind our socket port to the defined socket "server" where we define the port of the socket and the network
server.bind(ADDR)

# Function that handle any Client connect to the Server


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        # the First Msg recieved from the client which Set the number of the byte that will recieved by the server next which is the message itself so the Server be ready
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # if Statment to avoid the first empty message the clinet send to intiate the connection itself
        if msg_length:
            msg_length = int(msg_length)
            # The Certain Message that is send by the client is detected by its own length "msg_length"
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            output = None
            # the Algorithim that is Define as the order of the User
            if msg[0] == "A":
                output = "".join(sorted(msg[1 : len(msg)]))
            elif msg[0] == "D":
                output = "".join(sorted(msg[1 : len(msg)], reverse=True))
            elif msg[0] == "C":
                output = msg[1 : len(msg)].upper()
            else:
                output = msg
            # finaly the msg is encoded in the byte formate and resended to the User
            conn.send(output.encode(FORMAT))
    conn.close()


# The function that is responcible for the intialization of the Server and listen to the client connections


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # the server accept any connection and return the address of the connected client then add it to a thread then keep waiting to another client to connect
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()

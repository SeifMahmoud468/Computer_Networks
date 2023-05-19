import socket

HEADER = 64  # Number of byte first reseved by the Server
# Identify the Port number for the socket conncetion and the Server IP
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)  # define the ADDR for the Socket Connection
FORMAT = "utf-8"  # format of the encription
DISCONNECT_MESSAGE = "!DISCONNECT"  # the Disconnect msg that will close the TCP
# Define the socket itself by config the family of the socket which is defualt AF_INET which means internet network socket connection and the data Streaming
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Make the Connection to the Server
client.connect(ADDR)

# The Function that is responcible for sending the messages to the Server


def send(msg):
    # The message is encoded to be send and to get the number of byte needed to be recieved by the Server
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # The 'send_length' is the number of bytes that needed ny the server
    send_length += b" " * (HEADER - len(send_length))
    # the numebr of bytes needed is encoded then the rest of the header 64byte is added to the coded bytes to be fully recieved by the Server
    client.send(send_length)
    client.send(message)
    # the client recieved the responce of the server in 2048Bytes message
    print("\n")
    print(client.recv(2048).decode(FORMAT))
    print("\n")


# the function responcible for sending the disconnect msg to the server to close the TCP


def Disconnect():
    send(DISCONNECT_MESSAGE)


while True:
    choice = input(
        "Enter your choice:\n1- Send Message to server\n2- Disconnect from server\nYour Choice: "
    )
    if choice == "1":
        String = input("Enter your String: ")
        send(String)
    else:
        Disconnect()
        break

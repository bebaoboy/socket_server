import socket
from cryptography.fernet import Fernet

HEADER = 8
MAX_BUFFER_SIZE = 4096
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "end"
BROADCAST_MESSAGE = "[BROADCAST]"
ADMIN_NAME = ".ADMIN"
ADMIN_PASSWORD = "admin"
BLANK_MESSAGE = "NULL"
PACKET_LOSS = "Packet loss!"
QUIT = "quit"


def generate_key():
    # KEY = b"luminous" #14bytes
    key = b'749yEJF5VEhY12pQC80gUl5S3Y5euN5j7IbgYje4LSU='

    return key


fernet = Fernet(generate_key())


def receive(conn: socket, is_encode: bool = 0):
    full_msg = conn.recv(MAX_BUFFER_SIZE)
    i = 0
    h = HEADER
    msg_header = full_msg[:h]
    msg = ""
    try:
        while msg_header:
            msg_length = int(msg_header.strip())
            if len(msg_header):
                if is_encode:
                    msg += fernet.decrypt(full_msg[i + h:i + h + msg_length]).decode(FORMAT)
                else:
                    msg += full_msg[i + h:i + h + msg_length].decode(FORMAT)
                if msg != BLANK_MESSAGE:
                    i = h
                    h += HEADER

                    msg_header = full_msg[i:h]
    except:
        return msg
    return ""


# no except
def send(conn: socket, msg: str, is_encode: bool = 0):
    if not msg:
        msg = " "
    msg = msg.encode(FORMAT)
    if is_encode:
        msg = fernet.encrypt(msg)

    msg_header = f"{len(msg):<{HEADER}}".encode(FORMAT)

    conn.sendall(b"".join([msg_header, msg]))

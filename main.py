from server import start
import socket, sys
from utility.function import broadcast
from utility.sendreceive import *


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)
    server.setblocking(0)
    server.settimeout(5000)

    try:
        print("[STARTING] server is starting...")
        print(f"[LISTENING] Server is listening on {SERVER}")
        server.listen()
    except socket.error as err:
        print(f"Failed to connect socket to {SERVER}, port {PORT}")
        sys.exit()

    end_flag = False
    while not end_flag:
        num_of_client = []
        end_flag = start(server, num_of_client)

    print("[TERMINATED] Server is stopped!")
    server.close()


if __name__ == "__main__":
    main()


# client.py connect 192.168.1.8 port 5050


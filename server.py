import threading

from utility.sendreceive import *
from utility.function import command
from utility.util_list import client_list

THREAD_COUNT = threading.active_count()


def handle_client(conn: socket, addr, num_of_client: list):
    print(f"[NEW CONNECTION] {addr} entered the server.")

    try:  # first welcome
        send(conn, "Welcome to " + SERVER + "\n")
        name = ""

        send(conn, "Do you want to encrypt? (y/n)")
        if receive(conn) == 'y':
            is_encrypt = True
        else:
            is_encrypt = False

        send(conn, "\nThis session is "
             + ("not " if not is_encrypt else "")
             + "encrypted"
               '! \nWhat do you want to do?\nType "help" for instruction'
               '\nType "register" to create a new account\nOr press enter to receive notification',
             is_encrypt)

    except Exception as err:
        print(f"[{addr}] doesnt stay on welcome, disconnect abruptly")
        print(str(err))
        return

    activity_list = {
        "Battleship": 0,
        "Chat": 0
    }

    flag = []

    while True:
        try:  # awaiting response from client
            print(f"awaiting response from [{name}]")
            msg = receive(conn, is_encrypt)
            print(f"got response from [{name}]: {msg}\n")
        except Exception as err:
            print(f"[{addr}] doesnt response, disconnect abruptly")
            print(f"[{addr}] " + str(err))
            break

        try:

            if msg:
                if msg == DISCONNECT_MESSAGE:
                    print(f"[{addr}] gracefully left the server")
                    break

                elif msg == PACKET_LOSS:
                    send(conn, PACKET_LOSS, is_encrypt)

                else:
                    try:  # command-related
                        name = command(conn, msg, addr, activity_list, flag, is_encrypt, name)
                        # if(not name):
                        #     name = temp

                    except Exception as err:
                        print(f"[{addr}] " + str(err))
                        send(conn, str(err), is_encrypt)

                print(f"[{name}] finish command: {msg}\n")

        except Exception as err:
            print(f"[{addr}] cannot reach")
            print(str(err))
            break

    # after the while loop
    if name in client_list:
        client_list[name][3] = 0  # turn off online
    num_of_client.pop()

    print(f"[ACTIVE CONNECTIONS] {len(num_of_client)}")

    conn.close()


def start(server: socket, num_of_client: list):
    while True:
        try:  # timeout
            conn, addr = server.accept()
            conn.setblocking(1)
            client_msg = receive(conn)
            print(f"[NEW CONNECTION] {addr} detected with a message: ")
            print(client_msg, end="\n\n")

            temp = input("Continue to server? (y/n)")

            try:  # approval
                if temp == 'n':
                    print(f"[NEW CONNECTION] {addr} rejected")
                    send(conn, DISCONNECT_MESSAGE)
                    conn.close()
                    continue
                else:
                    send(conn, "Connecting to server...\n\n")
            except (Exception,):
                print(f"[{addr}] doesnt response, disconnect abruptly")
                continue

            print()

            try:  # threading
                thread = threading.Thread(target=handle_client,
                                          args=(conn, addr, num_of_client))
                num_of_client.append(1)
                length = len(num_of_client)
                print(f"[ACTIVE CONNECTIONS] {length}")
                thread.daemon = False
                thread.start()
            except Exception as err:
                print(f"[{addr}] cannot create thread\n" + str(err))
                send(conn, DISCONNECT_MESSAGE)
                conn.close()

        except (Exception,):
            print("[TIMEOUT] Server time out!")
            if input("Continue server (y/n): ") == 'n':
                return False

    return True

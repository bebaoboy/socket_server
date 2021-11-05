import threading
from utility.sendreceive import send, receive, DISCONNECT_MESSAGE
import sys
import socket


def is_encode(client: socket):
    temp = receive(client)
    print(temp)
    is_encrypt: bool
    _ = input()
    if _ == 'y':
        is_encrypt = True
    else:
        is_encrypt = False
    send(client, _)
    # temp = receive(client)
    # print(temp)
    return is_encrypt


def open_file():
    filename = input()
    with open(filename, 'r') as f:
        data: str = f.read()
    return data


def read(client: socket, is_encrypt: bool, prompt: list):
    while True:
        try:
            msg = receive(client, is_encrypt)
            if msg[:8] == "fromfwd ":
                # fromfwd sender to receiver msg
                words: list = msg.split()
                print(msg[len(words[0]) + len(words[1]) + len(words[2]) + len(words[3]) + 4:])
                # pair (sender, receiver)
                # print(words[1], " ", words[3])
                if len(prompt) == 1:
                    prompt[0] = (words[1], words[3])
                else:
                    prompt.append((words[1], words[3]))

            elif msg[:8] == "forward ":
                words: list = msg.split()
                msg = " ".join(words)
                send(client, msg, is_encrypt)

            elif msg[:9] == "no_reply ":
                # print more name
                # no_reply from sender to receiver
                words: list = msg.split()
                print(msg[len(f"no_reply from {words[2]} to {words[4]} ")])
                prompt.append("no_reply")

            elif msg[:6] == "reply ":
                prompt.clear()
                print(msg[6:])

            elif msg[:5] == "from ":
                # from sender to receiver msg
                words: list = msg.split()
                print(" ".join(words[4:]))
                # pair (sender, receiver)
                # print(words[1], " ", words[3])
                if len(prompt) == 1:
                    prompt[0] = (words[1], words[3])
                else:
                    prompt.append((words[1], words[3]))
            else:
                print(f"{msg}")
        except (Exception,):
            # print(str(err))
            # if input("Server is down. Exit (y/n)?") != 'n':
            #     #print("Connection closed!")
            #     client.close()
            #     # os.system('cls')
            break


def start(client: socket):
    # welcome screen
    temp = receive(client)
    print(temp)

    # encrypt or not
    try:
        is_encrypt = is_encode(client)
    except (Exception,):
        print("Error getting encode information. Server is busy!")
        return

    prompt = []

    # write_thread = threading.Thread(target = write, args = (client, is_encrypt, prompt, is_end))
    # write_thread.start()

    read_thread = threading.Thread(target=read, args=(client, is_encrypt, prompt))
    read_thread.start()

    while True:
        try:
            s = input(">>")
            if s == "open":
                try:
                    s = open_file()
                except (Exception,):
                    print("Invalid file")
                    continue

            # forward
            if len(prompt) > 0:
                if prompt[0] == "no_reply":
                    print("Please wait!")
                    continue
                # fromfwd sender to receiver msg
                sender, receiver = prompt[0]
                prompt.pop(0)
                # print(sender)
                s = f"forward {sender} from {receiver} " + s

            # reply sender msg
            if s[:6] == "reply ":
                if len(prompt) > 0:
                    sender, receiver = prompt[0]
                    prompt.pop(0)
                    # print(sender)
                    s = s[:6] + f"{sender} from {receiver} [{sender}]: " + s[6:]
                else:
                    print("No user to reply")

            elif s[:9] == "reply_all":
                if len(prompt) > 0:
                    sender = prompt[0][0]
                    prompt.pop(0)
                    # print(sender)
                    s = s[:9] + " " + sender
                else:
                    print("No user to reply")

            # print(f"Sending {s}")
            send(client, s, is_encrypt)

            if s == DISCONNECT_MESSAGE:
                break
        except (Exception,):
            if input("Server is down. Exit (y/n)?") != 'n':
                # os.system('cls')
                break

    print("Connection closed!")
    client.close()


def connect(server: str = "", port: int = 0):
    while True:
        conn: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if port == 0:
                server = input("\nEnter server's IP address: ")
                port = int(input("Enter server's port number: "))
            conn.connect((server, port))

        except (Exception,):
            print("Cannot connect. Invalid ip/port address")
            if input("Continue? (y/n): ") == 'n':
                break

        try:
            msg = input("Enter a short message for client to recognize you: ")
            if msg:
                send(conn, msg)
            else:
                send(conn, "None")
        except (Exception,):
            print("Server is down upon welcoming!")
            conn.close()
            if input("Continue? (y/n): ") == 'n':
                break

        # waiting for approval
        try:
            response = receive(conn)
            if response == DISCONNECT_MESSAGE:
                print("Server rejected!")
                conn.close()
                if input("Continue? (y/n): ") == 'n':
                    break
            else:
                print(response)

                return conn
        except (Exception,):
            print("Server doesnt response!")
            if input("Continue? (y/n): ") == 'n':
                break

    return None


# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def main(server: str = "", port: int = 0):
    client = connect(server, port)
    if client:
        start(client)
    else:
        print("Program exit")


# client.py connect <ip> port <port number>
if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) != 1 and (len(sys.argv) != 5 or sys.argv[1] != "connect" or sys.argv[3] != "port"):
        print("Invalid command line arguments")
    else:
        arg1 = sys.argv[2]
        arg2 = int(sys.argv[4])
        main(arg1, arg2)

# print( '{:*^30}'.format('centered')) ******center******

'''
    # main program
    while(True):
        #try:
        s = input(">>")
        if (s == "upload"):
            s = open_file()
        send(client, s, is_encrypt)
        if (s == DISCONNECT_MESSAGE):
            break 
        try:
            print("Waiting for response...\n")
            print(receive(client, is_encrypt))
        except (Exception,):
            if input("Continue to server (y/n)?") == 'n':
                break
        # except (Exception,):
        #     print("Error. Server is busy!")
        #     if ((input("Continue? (y/n): ")) != 'y'):
        #         break
        
    
def write(client:socket, is_encrypt:bool, prompt:list, is_end:list):
    sender=""
    while True:           
        s = input(">>")
        if s[:5] == "open ":
            try:
                file = open_file(s[5:])
                s = input("msg: ")
            except (Exception,):
                print("Invalid file")
                continue
        
        if len(prompt) > 0:
            sender = prompt[0]
            prompt.pop(0)
            print(sender)
            
        # reply sender msg
        if s[:6] == "reply ":
            s = s[:6] + sender + " " + s[6:] 
                
        print(f"Sending {s}")
        send(client, s, is_encrypt)
        
        if s == DISCONNECT_MESSAGE:
            print("Connection closed!")
            is_end[0] = 1
            client.close()
            break
            
    
def read(client:socket, is_encrypt:bool, prompt:list, is_end:list):
    sender= ""
    while is_end[0]!=1:
        try:
            msg = receive(client, is_encrypt)
            if msg[:5] == "from ": 
                words: list = msg.split()
                print(msg[5+len(words[1])+1:])
                prompt.append(words[1])
            else:
                print(f"Receiving: {msg}")
            #sleep(7)
        except (Exception,) except (Exception,)ion as err:
            #print(str(err))
            if input("Server is down. Exit (y/n)?") != 'n':
                print("Connection closed!")
                client.close()
                # os.system('cls')
                break


'''

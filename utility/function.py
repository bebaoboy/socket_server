from utility.sendreceive import ADMIN_PASSWORD, BROADCAST_MESSAGE, SERVER
from utility.gameUtil import start_game, approving_game, attack_ship, upload_ship, BATTLESHIP
from utility.communicate import *
from utility.help import show_help, help_util
from utility.showuser import show_active_clients, check_user
from utility.setup import setup_info


# need more try except
def register(connection, addr, is_encrypt: bool, name: str = ""):
    if name not in client_list:
        if not name:
            send(connection, "What should we call you? :", is_encrypt)
            name = receive(connection, is_encrypt)
        send(connection, "Enter your new password: ", is_encrypt)
        password = receive(connection, is_encrypt)
        while not password:
            send(connection, "Please enter your new password: ", is_encrypt)
            password = receive(connection, is_encrypt)

        # optional information
        send(connection, "Enter your fullname: ", is_encrypt)
        fullname = receive(connection, is_encrypt)
        send(connection, "Enter your dob dd/mm/yyyy: ", is_encrypt)
        dob = receive(connection, is_encrypt)
        send(connection, "Enter your bio (note): ", is_encrypt)
        note = receive(connection, is_encrypt)
        client_list[name] = [connection, addr,
                             Client(name, password,
                                    fullname if fullname else "",
                                    dob if dob else "",
                                    note if note else ""),
                             1, is_encrypt]
        send(connection, f"Registered. Welcome, {name}", is_encrypt)

    else:
        send(connection, f"User {name} has an account. Use login." + help_util("login"), is_encrypt)
    return name


# finished
def login(connection, addr, name, is_encrypt: bool):
    if name not in client_list:
        name = register(connection, addr, is_encrypt, name)

    else:
        if client_list[name][3] == 1:
            send(connection, f"User {name} already login", is_encrypt)

            return name
        while True:
            send(connection, f"\nLogin to {name}'s account.\nEnter your password: ", is_encrypt)
            password = receive(connection, is_encrypt)
            if client_list[name][2].password == password:
                send(connection, f"Welcome back, {name}!", is_encrypt)
                client_list[name][3] = 1  # turn back online
                client_list[name][4] = is_encrypt
                client_list[name][0] = connection
                client_list[name][1] = addr
                break

            else:
                send(connection, "Wrong password\nContinue (y/n): ", is_encrypt)
                if receive(connection, is_encrypt) != 'n':
                    continue
                else:
                    send(connection, "Exit login.", is_encrypt)
                    print(f"[{name}]: login failed.", is_encrypt)
                    name = ""
                    break
    return name


# finished, turn off online status
# socket send
def log_out(name):
    client_list[name][3] = 0
    send(client_list[name][0], "Log out successfully\n" +
         "Welcome to " + SERVER + "\n", client_list[name][4])


# encryption supported
# command option1 option2 option 3
# login username -> type 1 (must have at least 1 option)
def command(connection: socket, full_msg, addr, activity_list, flag: list, is_encrypt: bool = 0, name: str = ""):
    other_name = ""
    # forward sender from receiver msg
    if len(flag) > 0:
        try:
            other_name = flag[0][1]
            msg = full_msg
            if flag[0][0] == "Chat":
                # if len(word) > 1:
                #     msg = " ".join(word)
                if activity_list["Chat"] == 1:
                    word: list = full_msg.split()
                    msg = word[4]
                    approving_chat(connection, name, other_name, msg, is_encrypt, activity_list, flag)
                elif activity_list["Chat"] == 2:
                    begin_chat(connection, name, msg, is_encrypt, activity_list, flag)

            elif flag[0][0] == "Battleship":

                # if len(word) > 1:
                #     msg = " ".join(word)
                if activity_list["Battleship"] == 1:
                    word: list = full_msg.split()
                    msg = word[4]
                    approving_game(connection, name, other_name, msg,
                                   is_encrypt, activity_list, flag)
                elif activity_list["Battleship"] == 2 or activity_list[BATTLESHIP] == 3:
                    upload_ship(connection, name, other_name, msg, is_encrypt, activity_list, flag)
                elif activity_list["Battleship"] == 4:
                    attack_ship(connection, name, other_name, msg, is_encrypt, activity_list, flag)

        except Exception as err:
            send(connection, f"{other_name} left abruptly", is_encrypt)
            print(f"[{addr}]: {str(err)}")
            activity_list[flag[0][0]] = 0
            flag.clear()
        return name

    word: list = full_msg.split()
    if len(word) < 1:
        raise Exception('Missing command\nType "help" for instruction')
    commands = word[0]

    if commands not in command_list:
        raise Exception('Invalid command!\nType "help" for instruction')

    elif command_list[commands][0] > 0 and len(word) < 2:
        raise Exception(
            f"Missing command option for {commands}" + help_util(commands))

    elif commands != "to" and commands != "reply" and commands != "forward" and len(word) - 1 > len(
            command_list[commands][2:]):
        raise Exception(
            f"Too many command option for {commands}" + help_util(commands))

    else:
        try:
            if commands == "help":
                is_full = False if (len(word) == 2 and word[1] == "-short") else True
                show_help(connection, is_encrypt, is_full)

            elif commands == "logout":
                log_out(name)
                name = ""

            elif commands == "show_active_user":
                if name == "":
                    raise Exception("Please login to start a game." + help_util("login"))
                show_active_clients(connection, is_encrypt)

            elif commands == "register":
                name = word[1] if (len(word) == 2) else ""
                name = register(connection, addr, is_encrypt, name)

            elif commands == "login":
                # login username pass is_encrypt
                name = word[1]
                name = login(connection, addr, name, is_encrypt)

            # need login
            elif commands == "email":
                if name == "":
                    raise Exception("Please login to start a game." + help_util("login"))
                temp = word[1] if (len(word) == 2) else ""
                email(connection, name, temp, is_encrypt)

            elif commands == "reply":
                # reply sender from receiver msg
                other_name = word[1]
                msg = " ".join(word[4:])
                reply(name, other_name, msg)
                send(connection, "Sent", is_encrypt)

            elif commands == "to":
                if name == "":
                    raise Exception(
                        "Please login to start a game." + help_util("login"))
                other_name = word[1]
                msg = " ".join(word[2:])
                to(name, other_name, msg)
                send(connection, "Sent", is_encrypt)

            elif commands == "reply_all":
                temp = word[1]
                reply_all(connection, name, temp, is_encrypt)

            elif commands == "forward":
                other_name = word[1]
                # msg = " ".join(word)
                send(client_list[other_name][0], full_msg, client_list[other_name][4])

            # need login
            elif commands == "setup_info":
                if name == "":
                    raise Exception("Please login to start a game." + help_util("login"))
                # attention
                action = word[1]
                setup_info(connection, name, action, is_encrypt)

            elif commands == "check_user":
                if name == "":
                    raise Exception("Please login to start a game." + help_util("login"))
                username = word[1]
                action = word[2]
                check_user(connection, username, action, is_encrypt)

            elif commands == "chat":
                if name == "":
                    raise Exception(
                        "Please login to start a game." + help_util("login"))
                temp = word[1]
                chat(name, temp)
                flag.append(("Chat", temp))
                activity_list["Chat"] = 1

            # need login
            elif commands == "start_game":
                if name == "":
                    raise Exception("Please login to start a game." + help_util("login"))
                start_game(name, is_encrypt, activity_list, flag)

            # if admin...
        except Exception as err:
            raise Exception("Cannot precess command, " + str(err))

    return name


# encryption supported
# unfinished
def admin_command(connection: socket, is_encrypt: bool):
    send(connection, "Enter your password: ", is_encrypt)
    password = receive(connection)
    if password != ADMIN_PASSWORD:
        send(connection, "Wrong admin password!", is_encrypt)
        return


# encryption supported
# use name to find socket and is_encode
def broadcast(name: str, msg: str):
    for clients in client_list:
        if clients != name and client_list[clients][3] == 1:
            send(clients[0], BROADCAST_MESSAGE + msg, client_list[clients][4])

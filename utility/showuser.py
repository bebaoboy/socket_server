import socket

from utility.util_list import client_list
from utility.help import help_util
from utility.sendreceive import send


# finished no socket
# return a string of active client list
def active_client_list(name=""):
    active_user = ""
    for clients in client_list:
        if clients != name and client_list[clients][3] == 1:
            active_user += "\n" + clients
    return active_user


# finished
# socket send


def show_active_clients(conn: socket, is_encrypt: bool):
    active_user = "Active users:"
    active_user += active_client_list()
    send(conn, active_user, is_encrypt)


'''
    username = word[1]
    action = word[2]
    check_user(conn, username, action, is_encrypt)
'''


def check_user(conn: socket, username, action, is_encrypt: bool):
    if action == "-find":
        if username not in client_list:
            send(conn, "User not exists", is_encrypt)
        else:
            send(conn, "User exists", is_encrypt)

    elif action == "-online":
        if client_list[username][3] == 0:
            send(conn, f"{username} is active.", is_encrypt)
        else:
            send(conn, f"{username} is NOT active.", is_encrypt)

    if username not in client_list:
        raise Exception("Invalid user. Use this command: " + help_util("show_active_user"))

    if action == "-show_dob":
        send(conn, f"{username}'s dob is {client_list[username][2].dob}", is_encrypt)

    elif action == "-show_fullname":
        send(conn, f"{username}'s fullname is {client_list[username][2].fullname}", is_encrypt)

    elif action == "-show_note":
        send(conn, f"{username}'s bio is {client_list[username][2].note}", is_encrypt)

    elif action == "-show_all":
        send(conn, f"{username}'s everything is\n\
            fullname: {client_list[username][2].fullname}\n\
            dob: {client_list[username][2].dob}\n\
            note: {client_list[username][2].note}\n", is_encrypt)

    elif action == "-show_game":
        pass
    else:
        raise Exception("Invalid option." + help_util("check_user"))

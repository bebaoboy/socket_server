import socket
from utility.help import help_util
from utility.util_list import client_list
from utility.sendreceive import send, receive


def setup_info(conn: socket, name, action, is_encrypt: bool):
    if action == "-dob":
        send(conn, f"Your old dob: {client_list[name][2].dob}\nEnter your new dob: ", is_encrypt)
        new = receive(conn, is_encrypt)
        client_list[name][2].dob = new
        send(conn, f"Update dob successfully.\nYour new dob: {client_list[name][2].dob}", is_encrypt)

    elif action == "-fullname":
        send(conn, f"Your old fullname: {client_list[name][2].fullname}\nEnter your new fullname: ", is_encrypt)
        new = receive(conn, is_encrypt)
        client_list[name][2].fullname = new
        send(conn, f"Update fullname successfully.\nYour new fullname: {client_list[name][2].fullname}", is_encrypt)

    elif action == "-note":
        send(conn, f"Your old note: {client_list[name][2].note}\nEnter your new note: ", is_encrypt)
        new = receive(conn, is_encrypt)
        client_list[name][2].note = new
        send(conn, f"Update note successfully.\nYour new note: {client_list[name][2].note}", is_encrypt)

    else:
        raise Exception("Invalid option." + help_util("show_info"))

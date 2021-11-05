from time import sleep
from utility.util_list import *
from utility.help import help_util


# reply name of sender + raw message
def reply(name: str, other_name: str, msg: str):
    if (other_name not in client_list) or (client_list[other_name][3] == 0):
        raise Exception("Invalid user. Type show_active_user to see" + help_util("show_active_user"))

    print(f"[{name}] replying to {other_name}: {msg}")
    send(client_list[other_name][0], msg, client_list[other_name][4])


# command: to username msg
# format: from sender to receiver msg
def forward(sender: str, receiver: str, msg: str):
    if receiver not in client_list or client_list[receiver][3] == 0:
        # send(client_list[sender][0],
        #      "Invalid user to send.", client_list[sender][4])
        # return 0
        raise Exception("Invalid user to send.")

    print(f"[{sender}] forwarding to {receiver}: {msg}")

    msg = f"from {sender} to {receiver} " + msg
    send(client_list[receiver][0], msg, client_list[receiver][4])
    return 1


def to(sender: str, receiver: str, msg: str):
    if receiver not in client_list or client_list[receiver][3] == 0:
        # send(client_list[sender][0],
        #      "Invalid user to send.", client_list[sender][4])
        # return 0
        raise Exception("Invalid user to send.")

    print(f"[{sender}] forwarding to {receiver}: {msg}")

    msg = f"[{sender}]: " + msg
    forward(sender, receiver, msg)
    return 1


def forward_no_reply(sender: str, receiver: str, msg: str):
    if receiver not in client_list or client_list[receiver][3] == 0:
        # send(client_list[sender][0],
        #      "Invalid user to send.", client_list[sender][4])
        # return 0
        raise Exception("Invalid user to send.")

    print(f"[{sender}] forwarding no_reply to {receiver}: {msg}")

    msg = f'no_reply from {sender} to {receiver} ' + msg
    send(client_list[receiver][0], msg, client_list[receiver][4])
    return 1


def reply_all(connection, name, other_name, is_encode):
    end_chat = "send chat"
    msg = []

    send(connection, 'Enter your message, "send chat" to finish', is_encode)

    forward(name, other_name, f'[{name}] send you a message:\n')

    while True:
        temp = receive(connection, is_encode)
        if temp == end_chat:
            send(connection, "Send successfully", is_encode)
            break
        msg.append(temp)
        send(connection, "", is_encode)

    try:
        while len(msg) > 0:
            forward_no_reply(name, other_name, f"[{name}]: " + msg[0])
            msg.pop(0)
            sleep(.5)
        forward(name, other_name, "End of message")

    finally:
        raise Exception(f"{other_name} disconnect")


# finished
def email(connection, name: str, other_name: str, is_encode: bool):
    if (other_name not in client_list) or (client_list[other_name][3] == 0):
        raise Exception("Invalid user to chat with")

    # awaiting receiver receive from main server
    reply_all(connection, name, other_name, is_encode)


# all valid sender and receiver
def forward_reforward(sender, receiver, msg):
    print(f"[{sender}] forwarding re_forward to {receiver}: {msg}")

    msg = f'fromfwd {sender} to {receiver} ' + msg
    send(client_list[receiver][0], msg, client_list[receiver][4])


def chat(name, other_name):
    # send invitation (flag = 1)
    if other_name not in client_list or client_list[other_name][3] == 0:
        raise Exception("Invalid user to chat with.")

    forward_reforward(name, other_name, f"{name} wants to chat with you\nType yes to accept.")
    forward_no_reply(name, name, "Waiting for response...")


def approving_chat(connection, name, other_name, msg, is_encode, activity_list: dict, flag: list):
    print(f"[{name}] approving chat received from {other_name}: {msg}")
    # if accept -> flag == 2
    if msg == "yes":
        activity_list["Chat"] = 2
        reply(name, name, f"reply Hey, {other_name} accepted.")
        send(connection, "Chat and enter to send. Type cancel to end chat", is_encode)
        forward_reforward(name, other_name, f"Chat with {name} and enter to send. Type cancel to end chat")

    else:
        activity_list["Chat"] = 0
        flag.clear()
        send(connection, f"{other_name} denied to chat", is_encode)
        reply(name, name, "reply ")


def begin_chat(connection, name, msg, is_encode, activity_list: dict, flag: list):
    other_name = flag[0][1]

    if msg != "cancel":
        if msg[:8] == "forward ":  # they chat
            if msg[len(f"forward {name} from {other_name} "):] == "cancel":  # they cancel
                send(connection, f"[{other_name}]: left the chat", is_encode)
                flag.clear()
                activity_list["Chat"] = 0
            else:
                forward_reforward(name, other_name, "Sent")
                send(connection, f"[{other_name}]: " + msg[len(f"forward {name} from {other_name} "):], is_encode)

        else:  # me chat
            send(connection, "Sent", is_encode)
            forward_reforward(name, other_name, f"[{name}]: " + msg)
    else:
        # if msg[:8] == "forward ":  # they chat
        #     # forward_reforward(name, other_name, "Sent")
        #     send(conn, f"[{other_name}]: left the chat", is_encode)

        # me cancel
        # send(conn, "Sent", is_encode)
        send(client_list[other_name][0], f"[{name}] left the room", client_list[other_name][4])
        reply(name, other_name, "reply ")
        flag.clear()
        activity_list["Chat"] = 0

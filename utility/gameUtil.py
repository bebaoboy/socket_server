from model.ship import Ship
from utility.showuser import active_client_list
from utility.sendreceive import QUIT
from utility.communicate import *

BATTLESHIP = "Battleship"
BOARD_SIZE = 21

# AcroName = {1: "Ship 1", 2: "Ship 2", 3: "Ship 3", 4: "Ship 4", 5: "Ship 5", 6: "Ship 6", 7: "Ship 7",
#       8: "Ship 8", 9: "Ship 9", 10: "Ship 10", 11: "Ship 11", 12: "Ship 12"}

ship_alphabet = {
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
    "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19
}


def create_room(name, is_encode1):
    connection = client_list[name][0]
    active_list = active_client_list(name)
    active_list += "\nEnter one user name: "

    # send to player 1 to pick a player
    send(connection, active_list, is_encode1)

    # neu player1 nhap sai ten
    # receive the player2
    other_name = receive(connection, is_encode1)
    while other_name not in client_list and name == other_name:
        send(connection, "Invalid user. Continue (y/n)?" + active_list, is_encode1)
        other_name = receive(connection, is_encode1)
        if other_name == 'n':
            return None, None

    return other_name, client_list[other_name][4]


def start_game(name, is_encode1, activity_list: dict, flag: list):
    other_name, is_encode2 = create_room(name, is_encode1)
    if not other_name:
        return

    activity_list[BATTLESHIP] = 1
    flag.append((BATTLESHIP, other_name))

    forward_reforward(name, other_name,
                      f"{name} wants to play Battleship with you\nType yes to accept.")
    forward_no_reply(name, name, "Waiting for response...")


def approving_game(connection, name, other_name, msg,
                   is_encode, activity_list, flag):
    print(f"[{name}] game accept received from {other_name}: {msg}")
    # if accept -> flag == 2
    if msg == "yes":
        activity_list[BATTLESHIP] = 2
        reply(name, name, f"reply Hey, {other_name} accepted.")
        send(connection, "Upload your ship. Type cancel to quit the game.", is_encode)
        forward_no_reply(
            name, other_name, f"Waiting for {name} to upload their ships...")

    else:
        activity_list[BATTLESHIP] = 0
        flag.clear()
        send(connection, f"{other_name} denied to play", is_encode)
        reply(name, name, "reply ")


def show_board(name):
    s = ""
    for row in client_list[name][2].battleship.board:
        for col in row:
            s += f"{col :<6}"

        s += '\n'

    return s


# finished
def create_ship_list(name, ships):
    ship_list = []
    lines = ships.split('\n')
    for line in lines:
        word = line.split()
        ship_list.append(Ship(int(word[0]), int(word[1]), int(word[2]) + 1, int(word[3]) + 1))

    client_list[name][2].battleship.ship = ship_list
    client_list[name][2].battleship.num_of_ship = len(ship_list)


def upload_ship(connection, name, other_name, msg, is_encrypt, activity_list, flag):
    if msg[:8] != "forward ":
        ship_list = msg
        if msg == QUIT:
            activity_list[BATTLESHIP] = 0
            flag.clear()
            send(connection, "You quit the game", is_encrypt)
            send(client_list[other_name][0], f"{name} quits the game", client_list[other_name][4])
        else:
            create_ship_list(name, ship_list)
            initial_board(name)
            b = show_board(name)
            print(b)
            forward_no_reply(name, name, f"Your board:\n" + b
                             + f"\nWaiting for {other_name} to upload their ships")
            forward_reforward(name, other_name, "Upload your ship. Type cancel to quit the game.")
    else:
        ship_list = msg[len(f"forward {name} from {other_name} "):]
        if msg[len(f"forward {name} from {other_name} "):] == QUIT:
            activity_list[BATTLESHIP] = 0
            flag.clear()
            send(connection, f"{other_name} quits the game", is_encrypt)
            send(client_list[other_name][0], "you quits the game", client_list[other_name][4])
        else:
            activity_list[BATTLESHIP] = 2
            create_ship_list(other_name, ship_list)
            initial_board(other_name)
            b = show_board(other_name)
            reply(name, name, f"reply Game begins. Your board:\n{b}\nYou go first!\n")
            send(connection, "Attack their ship (x,y). Type cancel to quit the game:", is_encrypt)
            forward_no_reply(
                name, other_name, f"Game begins.\nYour board:\n"
                                  + b + f"\n{name} goes first. Wait for your turn...\n")


# finished
def initial_board(name):
    board = [['.' for __ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    # print(board)
    board[0][0] = ' '
    for i in range(1, BOARD_SIZE):
        board[0][i] = str(i)
    for i in range(1, BOARD_SIZE):
        board[i][0] = chr(97 - 32 + i - 1)

    for obj in client_list[name][2].battleship.ship:
        for k in obj.representOfShip:
            board[k[0]][k[1]] = 'X'
    client_list[name][2].battleship.board = board


def increase_score(name):
    client_list[name][2].battleship.score += 1


def update_board(hit_index, hit_object, miss_index, name):
    player = client_list[name][2]
    if hit_index:
        player.battleship.board[hit_index[0]][hit_index[1]] = 'H'
        increase_score(name)
        for m in hit_object.representOfShip:
            player.battleship.board[m[0]][m[1]] = 'S'
            # increase_score(name)
    if miss_index:
        player.battleship.board[miss_index[0]][miss_index[1]] = 'M'


def show_hit_miss(name):
    player = client_list[name][2].battleship
    return f"\nHit: {len(player.hit)}, Miss: {len(player.miss)}\n"


def show_remaining_ship(name):
    player = client_list[name][2].battleship
    return f"\nShip remaining: {len(player.ship)}\n"


# Todo
# Need to check for more runtime check

def hit_or_miss(x, y, name: str):
    # neu trung thi se add vao hit cua thang ban
    # tang diem cua thang ban trung
    hit = False
    player = client_list[name][2].battleship

    coordinate = [int(x), int(y)]
    for obj in player.ship:
        for k in obj.representOfShip:
            if k == coordinate:
                player.battleship.hit.append(k)
                update_board(k, obj, 0, player)
                hit = True

    if hit:
        return True
    else:
        player.battleship.miss.append(coordinate)
        update_board(0, player.ship, coordinate, player)
        return False


def is_lose(name):
    return client_list[name][2].battleship.num_of_ship == 0


def attack_ship(connection, name, other_name, msg: str, is_encrypt, activity_list, flag):
    if len(msg) >= 8 and msg[:8] != "forward ":  # you attack
        if msg == QUIT:
            activity_list[BATTLESHIP] = 0
            flag.clear()
            send(connection, "You quit the game", is_encrypt)
            send(client_list[other_name][0], f"{name} quits the game. You win!", client_list[other_name][4])
            client_list[other_name][2].game.append((BATTLESHIP, name, -1))
            client_list[other_name][2].battleship.score = -1
            client_list[name][2].game.append((BATTLESHIP, other_name, -1))
            client_list[name][2].battleship.score = -1
        else:
            word = msg.split()
            if (client_list[other_name][2].battleship.board[word[0]][word[1]] == '.') \
                    or (int(word[0]) < 1 or int(word[0]) > BOARD_SIZE - 1) \
                    or (int(word[1]) < 1 or int(word[1]) > BOARD_SIZE - 1):  # I already shot
                send(connection, "Invalid coordinates", is_encrypt)
                return
            if is_lose(other_name):  # you win
                client_list[other_name][2].game_list.append(
                    (BATTLESHIP, name, client_list[other_name][2].battleship.score))
                client_list[name][2].game_list.append((BATTLESHIP, other_name, client_list[name][2].battleship.score))

            if hit_or_miss(word[0], word[1], other_name):
                send(connection, f"Hit. One ship down. {show_remaining_ship(other_name)}Attack (x,y):")
                forward_no_reply(name, other_name, f"{name} shot your ship at ({word[0], word[1]} \
                                                   {show_remaining_ship(other_name)}")
            else:
                forward_no_reply(name, name, f"You missed. {show_hit_miss(name)} Waiting for other to shoot...")
                forward_reforward(name, other_name,
                                  "Your board:\n" + show_board(other_name) + f"\n{name} missed. Your turn, attack(x,y).\
                                        \nType cancel to quit the game: ")
    else:  # they attack
        if msg[len(f"forward {name} from {other_name} "):] == QUIT:
            activity_list[BATTLESHIP] = 0
            flag.clear()
            send(connection, f"{other_name} quits the game. You win", is_encrypt)
            send(client_list[other_name][0], f"you quits the game", client_list[other_name][4])
            client_list[other_name][2].game_list.append((BATTLESHIP, name, -1))
            client_list[other_name][2].battleship.score = -1
            client_list[name][2].game_list.append((BATTLESHIP, other_name, -1))
            client_list[name][2].battleship.score = -1
        else:
            word = msg.split()
            if (client_list[other_name][2].battleship.board[word[0]][word[1]] == '.') \
                    or (int(word[0]) < 1 or int(word[0]) > BOARD_SIZE - 1) \
                    or (int(word[1]) < 1 or int(word[1]) > BOARD_SIZE - 1):
                forward_reforward(name, other_name, "Invalid coordinates")
                return
            if is_lose(name):  # you win
                client_list[other_name][2].game.append(
                    (BATTLESHIP, name, client_list[other_name][2].battleship.score))
                client_list[name][2].game.append((BATTLESHIP, other_name, client_list[name][2].battleship.score))

            if hit_or_miss(word[0], word[1], name):
                send(connection, f"Hit. One ship down. {show_remaining_ship(name)}Attack (x,y):")
                forward_no_reply(name, other_name, f"{other_name} shot your ship at ({word[0], word[1]} \
                                                   {show_remaining_ship(name)}")
            else:
                forward_no_reply(name, name, f"You missed. {show_hit_miss(other_name)} Waiting for other to shoot...")
                forward_reforward(name, other_name,
                                  "Your board:\n" + show_board(name) + f"\n{other_name} missed. Your turn, attack(x,y).\
                                        \nType cancel to quit the game: ")


'''
    # def find_user(connection: socket, player1: str):
    #     active_list = show_active_clients(player1)
    #     active_list += "\nEnter one user name: "

    #     # send to player 1 to pick a player
    #     send(connection, active_list, client_list[player1][5])

    #     # Todo
    #     # neu player1 nhap sai ten
    #     # receive the player2
    #     player2_name = receive(connection, client_list[player1][5])
    #     while player2_name not in client_list:
    #         send(connection, "Invalid user. Continue (y/n)?" + active_list, client_list[player1][5])
    #         player2_name = receive(connection, client_list[player1][5])
    #         if player2_name == 'n':

    #     return player2_name, client_list[player2_name][0]
'''

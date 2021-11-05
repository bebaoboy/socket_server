import socket

from utility.sendreceive import DISCONNECT_MESSAGE, send, receive
from model.battleship import BattleShip

conn: socket = None


class Client:
    def __init__(self, username="", password="", fullname="", dob: str = "", note: str = ""):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.dob = dob
        self.note = note
        self.game = []  # game, players, score
        self.battleship = BattleShip()

    def add_game(self, game, players: list, score: int):
        self.game[game] = [game, players, score]

    def edit_dob(self, connection, is_encrypt):
        send(connection, "Enter your new dob: ", is_encrypt)
        dob = receive(connection, is_encrypt)
        if dob:
            self.fullname = dob

    def edit_fullname(self, connection, is_encrypt):
        send(connection, "Enter your new fullname: ", is_encrypt)
        fullname = receive(connection, is_encrypt)
        if fullname:
            self.fullname = fullname


# command : [type, "description", dict("first option", "explanation"), ...]
command_list = {
    "register": [0, "for registration",
                 {
                     "<username>": "name of user to register (not required)\nUser name must NOT contain a space"
                 }
                 ],

    "login": [1, "for login",
              {
                  "<username>": "name of user to login"
              }
              ],

    "setup_info": [1, "for modifying your profile",
                   {
                       "-online": "setting online status",
                       "-dob": "edit date of birth",
                       "-fullname": "edit fullname",
                       "-note": "edit bio",
                   }
                   ],

    "check_user": [2, "for checking a user's profile",
                   {
                       "<username>": "name of user, can be YOUR NAME also"
                   },
                   {
                       "-find": "check existence of user",
                       "-online": "check online status",
                       "-show_dob": "show date of birth",
                       "-show_fullname": "show fullname",
                       "-show_note": "show bio",
                       "-show_all": "show full profile",
                       "-show_game": "show user's gameplay status"
                   }
                   ],
    "chat": [1, "for chatting with another user",
             {
                 "<username>": 'name of user (dont type in username to chat with server)'
             }
             ],
    "email": [1, "for sending email with another user",
              {
                  "<username>": 'name of user'
              }
              ],
    "reply": [1, "for replying who just texted you",
              {
                  "<message>": "message from you"
              }
              ],
    "reply_all": [1, "for replying a big message to whom just texted you",
                  {
                      "<username>": "who you reply to"
                  }
                  ],
    "forward": [1, "unused",
                {
                    " ": " "
                }
                ],
    "to": [2, "for sending direct message",
           {
               "<username>": "who you send to"
           },
           {
               "<message>": "message from you"
           }
           ],
    "help": [0, "for open help panel", {
        "-short": "quick reference (not required)",
        "-full": "full help panel (default)"
    }],
    DISCONNECT_MESSAGE: [0, "for close connection"],
    "show_active_user": [0, "for show active user"],
    "logout": [0, "for login out of current user"],
    "start_game": [1, "for starting the game",
                   {
                       "<name>": "name of the game in Camel Case"
                   }],
    "end": [0, "for end the session. Leave the option empty to END THE SESSION"]
}

# name = socket, addr, Client, is_online, is_encode
# edit
client_list = {
    "quan": [conn, "192.168.1.1", Client("quan", "hi", "luu tuan quan", "01/01/2002", "hi mn"), 0, 0],
    "bao": [conn, "192.168.1.1", Client("bao", "hi", "huynh minh bao", "01/02/2002", "chao tat ca cac ban"), 0, 0]
}

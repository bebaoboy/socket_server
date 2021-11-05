from utility.util_list import *


# finished
def help_util(command: str):
    help_msg: str = "\n"
    help_msg += "<" + command + ">: "
    help_msg += command_list[command][1]  # description
    mandatory_option = command_list[command][0]
    help_msg += f" (required: {mandatory_option} option)"

    if mandatory_option:  # type
        idx = 1
        # option list -> i is dict
        for dictionary in command_list[command][2:]:
            help_msg += "\n" + " "*4 + f"option {idx}:"
            for item in dictionary:  # option item in dict
                help_msg += "\n" + " "*8
                help_msg += item + ": "  # name
                help_msg += dictionary[item]
            help_msg += "\n"
            idx += 1
    help_msg += "\n"
    return help_msg


def show_help(connection, is_encrypt: bool, is_full: bool = 1):
    help_msg = "\n====\n\n\
    Usage: type in the command along with some number of options(as required by each command)\n\
    <command> <option1> <option2>...\n\
    Example: check_user minhbao -show_dob\n\n\
    ====\n\n\
    Available <commands>:\n"
    if is_full:
        for command in command_list:  # original
            help_msg += help_util(command)
    else:
        for command in command_list:
            help_msg += command + ": "
            mandatory_option = command_list[command][0]
            help_msg += f" (required: {mandatory_option} option)"

            if mandatory_option:  # type
                idx = 1
                # option list -> i is dict
                for dictionary in command_list[command][2:]:
                    help_msg += "\n" + " "*4 + f"option {idx}:"
                    for item in dictionary:  # option item in dict
                        help_msg += "\n" + " "*8
                        help_msg += item + " "  # name
                    help_msg += "\n"
                    idx += 1
            help_msg += "\n"

    send(connection, help_msg, is_encrypt)

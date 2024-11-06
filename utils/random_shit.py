from data import constants as Constants

def print_welcome_box():
    """
    Do some random shits. Good luck.
    """
    messages = [
        "Welcome to GOOPi Bot!",
        f"{Constants.CONST_APP_VERSION}",
        "Made by Trevor"
    ]
    
    top_border_char = "="
    side_border_char = "∥"
    padding = 2

    # Determine the width based on the longest message
    max_message_length = max(len(message) for message in messages)
    width = max_message_length + padding * 2 + 2  # 2 extra for side borders

    # Top border
    print(top_border_char * width)

    # Message lines with padding
    for message in messages:
        print(side_border_char + " " * padding + message.ljust(max_message_length) + " " * padding + side_border_char)

    # Bottom border
    print(top_border_char * width)
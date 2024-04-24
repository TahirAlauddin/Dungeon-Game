class CommandWords:
    """
    This class holds a set of all command words known to the game.
    It is used to recognise commands as they are typed in.
    """

    def __init__(self):
        """Constructor - initialise the command words"""
        self.__valid_commands = [
            "go",
            "quit",
            "help",
            "pick",
            "drop",
            "back",
            "give",
            "fight",
            "status",
        ]

    def is_command(self, a_string):
        """Check whether a given String is a valid command word.

        Returns true if it is, false if it isn't.
        """
        return a_string in self.__valid_commands

    def show_all(self):
        """Print all valid commands to the screen"""
        for command in self.__valid_commands:
            print(command + ", ", end="")
            # 'end' is a keyword argument that determines the character printed at the end of the string
            # This defaults to the newline character but here we are setting it to the blank string
            # This means each command follows the previous one on the same line
        print()
        # Now we print nothing - this is just to print a newline character

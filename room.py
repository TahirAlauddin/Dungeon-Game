"""
 * Class Room - a room in an adventure game.
 *
 * This class is part of the "World of Zuul" application. 
 * "World of Zuul" is a very simple, text based adventure game.  
 *
 * A "Room" represents one location in the scenery of the game.  It is 
 * connected to other rooms via exits.  For each existing exit, the room 
 * stores a reference to the neighboring room.
 * 
"""


class Room:
    """A "Room" represents one location in the scenery of the game.  It is
    connected to other rooms via exits.  For each existing exit, the room
    stores a reference to the neighboring room.
    """

    def __init__(self, description):
        """Create a room described "description". Initially, it has
        no exits. "description" is something like "a kitchen" or
        "an open court yard".

        Paramaters
        ----------
        description: string
            The room's description
        """
        self.__description = description
        self.__exits = {}

    def set_exit(self, direction, neighbour):
        """Define an exit from this room.

        Parameters
        ----------
        direction: string
            The direction of the exit
        neighbour: Room
            The room to which the exit leads
        """
        self.__exits[direction] = neighbour

    def get_short_description(self):
        """Returns The short description of the room
        (the one that was defined in the constructor).
        """
        return self.__description

    def get_long_description(self):
        """Return a description of the room in the form:
        You are in the kitchen.
        Exits: north west

        Returns A long description of this room
        """
        return "You are in the " + self.__description + ".\n" + self.get_exit_string()

    def get_exit_string(self):
        """Return a string describing the room's exits, for example
        "Exits: north west".

        Returns Details of the room's exits.
        """
        return_string = "Exits:"
        for room_exit in self.__exits.keys():
            return_string += " " + room_exit
        return return_string

    """
     * Return the room that is reached if we go from this room in direction
     * "direction". If there is no room in that direction, return None.
     *     direction The exit's direction.
     *     Returns The room in the given direction.
    """

    def get_exit(self, direction):
        """Return the room that is reached if we go from this room in direction
        "direction". If there is no room in that direction, return None.

        Parameters
        ----------
        direction: string
            direction The exit's direction.

        Returns The room in the given direction.
        """
        if direction in self.__exits:
            return self.__exits[direction]
        else:
            return None  # None is a special Python value that says the variable contains nothing

    @property
    def exits(self):
        return self.__exits

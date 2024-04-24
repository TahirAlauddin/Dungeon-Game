from room import Room


class Map:
    def __init__(self) -> None:
        self.__map = {
            1: Room("Room # 1"),
            2: Room("Room # 2"),
            3: Room("Room # 3"),
            4: Room("Room # 4"),
            5: Room("Room # 5"),
            6: Room("Room # 6"),
            7: Room("Room # 7"),
            8: Room("Room # 8"),
            9: Room("Room # 9"),
            10: Room("Room # 10"),
            11: Room("Room # 11"),
            12: Room("Room # 12"),
            13: Room("Room # 13"),
            14: Room("Room # 14"),
            15: Room("Room # 15"),
        }

    def link_exits(self):
        """Add exits to the rooms in the dungeon"""
        # Start room
        self.__map[1].set_exit("east", self.__map[2])
        self.__map[1].set_exit("south", self.__map[4])

        # Room 2
        self.__map[2].set_exit("west", self.__map[1])
        self.__map[2].set_exit("south", self.__map[5])

        # Room 3
        self.__map[3].set_exit("south", self.__map[6])

        # Room 4
        self.__map[4].set_exit("north", self.__map[1])
        self.__map[4].set_exit("south", self.__map[7])

        # Room 5
        self.__map[5].set_exit("north", self.__map[2])
        self.__map[5].set_exit("south", self.__map[8])
        self.__map[5].set_exit("east", self.__map[6])

        # Room 6
        self.__map[6].set_exit("north", self.__map[3])
        self.__map[6].set_exit("south", self.__map[9])

        # Room 7
        self.__map[7].set_exit("north", self.__map[4])
        self.__map[7].set_exit("east", self.__map[8])

        # Room 8
        self.__map[8].set_exit("south", self.__map[11])
        self.__map[8].set_exit("north", self.__map[5])
        self.__map[8].set_exit("west", self.__map[7])
        self.__map[8].set_exit("east", self.__map[9])

        # Room 9
        self.__map[9].set_exit("north", self.__map[6])
        self.__map[9].set_exit("south", self.__map[12])
        self.__map[9].set_exit("west", self.__map[8])

        # Room 10
        self.__map[10].set_exit("east", self.__map[11])
        self.__map[10].set_exit("south", self.__map[13])

        # Room 11
        self.__map[11].set_exit("north", self.__map[8])
        self.__map[11].set_exit("south", self.__map[14])
        self.__map[11].set_exit("east", self.__map[12])
        self.__map[11].set_exit("west", self.__map[10])

        # Room 12
        self.__map[12].set_exit("north", self.__map[9])
        self.__map[12].set_exit("west", self.__map[11])

        # Room 13
        self.__map[13].set_exit("north", self.__map[10])

        # Room 14
        self.__map[14].set_exit("north", self.__map[11])
        self.__map[14].set_exit("east", self.__map[15])

        # Room 15
        self.__map[15].set_exit("west", self.__map[14])

    """
     * Defining dunder methods so we can do different operations 
     * on the Map object
    """

    def __getitem__(self, item):
        """This method makes the class able to get key value pair
        >>> map = Map()
        >>> map[1]
        <room.Room object at 0x0000023089C28550>
        >>> print(map[1].get_long_description())
        You are in the Room # 1.
        Exits: south east"""
        return self.__map[item]

    def __iter__(self):
        """Returns an iterator of the dictionary"""
        return iter(self.__map)

    def __len__(self):
        """Returns the length of the map i.e. the number of Rooms"""
        return len(self.__map)

    @property
    def rooms(self):
        return self.__map
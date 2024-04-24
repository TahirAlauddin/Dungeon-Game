from itertools import chain
from random import choice
from room import Room
from command import Command
from command_parser import Parser
from objects import *
from map import Map
from constants import *
import sys

"""
 *  This class is the main class of the "World of Zuul" application. 
 *  "World of Zuul" is a very simple, text based adventure game.  Users 
 *  can walk around some scenery. That's all. It should really be extended 
 *  to make it more interesting!
 * 
 *  To play this game, create an instance of this class and call the "play"
 *  method.
 * 
 *  This main class creates and initialises all the others: it creates all
 *  rooms, creates the parser and starts the game.  It also evaluates and
 *  executes the commands that the parser returns.
"""


class Game:
    """To play this game, create an instance of this class and call the "play"  method.
    This main class creates and initialises all the others: it creates all
    rooms, creates the parser and starts the game. It also evaluates and
    executes the commands that the parser returns.
    """

    item_types = ["food", "herb"]
    weapon_types = ["sword", "spear"]
    monster_types = ["goblin", "orc", "wolf"]
    items: List[Item] = []
    monsters: List[Monster] = []
    weapons: List[Weapon] = []
    magical_transporter_room: Room = None
    last_room: Room = None
    # Key to get to Room # 15
    key = False

    def __init__(self):
        """Create the game and initialise its internal map."""
        # Rooms must be created first; then place items etc.
        self.player = Player(PLAYER_HP)
        self.create_rooms()
        self.place_items()
        self.place_weapons()
        self.place_monsters()
        self.place_dwarf()
        self.__parser = Parser()

    def create_rooms(self):
        """Create all the rooms and link their exits together."""
        # create the map
        self.map = Map()
        self.map.link_exits()

        # Set magic transporter room to Room # 3
        self.magical_transporter_room = self.map[3]

        # Set exit room to Room # 15
        self.exit_room = self.map[15]

        # We can use key value pairs in Map which should return Room object
        # Current room is start_room
        self.__current_room = self.map[START_ROOM]

    def place_items(self):
        """Randomly place items on the map"""

        for i in range(FOOD_ITEMS):
            room = self.get_random_room()  # random Room
            item = Item(
                f"Food # {i+1}", FOOD_DESCRIPTION, room, choice(range(20, 110, 10))
            )
            self.items.append(item)

        for i in range(NUM_OF_HERBS):
            room = self.get_random_room()  # random Room
            item = Item(
                f"Herb # {i+1}", HERBS_DESCRIPTION, room, choice(range(20, 110, 10))
            )
            self.items.append(item)

    def place_weapons(self):
        """Randomly place weapons on the map"""
        for i in range(SWORD):
            room = self.get_random_room()  # random Room
            if i == 0:
                room = self.map[1]  # Start Room
            weapon = Weapon(
                f"Sword # {i+1}",
                WEAPON_DESCRIPTION,
                room,
                choice(range(20, 110, 10)),
                SWORD_HP,
            )
            self.weapons.append(weapon)

        for i in range(SPEAR):
            room = self.get_random_room()  # random Room
            weapon = Weapon(
                f"Spear # {i+1}",
                WEAPON_DESCRIPTION,
                room,
                choice(range(20, 110, 10)),
                SPEAR_HP,
            )
            self.weapons.append(weapon)

    def place_dwarf(self):
        """Randomly place dwarf on the map"""
        room = self.get_random_room()  # random Room
        self.dwarf = Dwarf(f"Dwarf", DWARF_DESCRIPTION, room)

    def place_monsters(self):
        """Randomly place monsters on the map"""

        for i in range(GOBLINS):
            room = self.get_random_room()  # random Room
            monster = Monster(f"Goblin # {i+1}", MONSTER_DESCRIPTION, room, GOBLIN_HP)
            self.monsters.append(monster)

        for i in range(ORCS):
            room = self.get_random_room()  # random Room
            monster = Monster(f"Orc # {i+1}", MONSTER_DESCRIPTION, room, ORC_HP)
            self.monsters.append(monster)

        for i in range(WOLVES):
            room = self.get_random_room()  # random Room
            monster = Monster(f"Wolf # {i+1}", MONSTER_DESCRIPTION, room, WOLF_HP)
            self.monsters.append(monster)

    def print_objects_in_current_room(self):
        objects = self.get_objects_in_room(self.__current_room)
        print("This room has following objects:\n")
        print("Items:", ", ".join([str(item) for item in objects["Items"]]))
        print("Weapons:", ", ".join([str(weapon) for weapon in objects["Weapons"]]))
        print("Monsters:", ", ".join([str(monster) for monster in objects["Monsters"]]))

        if self.dwarf and (self.dwarf.get_room() == self.__current_room):
            print("The Dwarf")

    def print_welcome(self):
        """Print out the opening message for the player"""
        print()
        print("Welcome to the World of Zuul!")
        print("World of Zuul is a new, incredibly boring adventure game.")
        print("Type 'help' if you need help.")
        print()
        print(self.__current_room.get_long_description())

    def process_command(self, command: Command):
        """Given a command, process (that is: execute) the command.
        Returns true If the command ends the game, false otherwise.
        """
        want_to_quit = False

        if command.is_unknown():
            print("I don't know what you mean...")
            return False

        command_word = command.get_command_word()
        if command_word == "help":
            self.print_help()
        elif command_word == "go":
            self.go_room(command)
        elif command_word == "quit":
            want_to_quit = self.quit(command)
        elif command_word == "give":
            self.give_item(command)
        elif command_word == "pick":
            self.pick_item(command)
        elif command_word == "drop":
            self.drop_item(command)
        elif command_word == "back":
            self.go_back()
        elif command_word == "fight":
            self.fight()
        elif command_word == "status":
            self.status()

        return want_to_quit

    # implementations of user commands:

    def print_help(self):
        """Print out some help information."""
        print("|\tYou are alone. You wander")
        print("|\taround at the Dungeon trying to find an exit.")
        print("|\tIn order to win, you need to get the key from ")
        print("|\tthe Dwarf and get to the exit room safely.")
        print("|\tThe Dwarf is blind, he needs some food to eat")
        print("|\tand herbs to cure his eyes.")
        print("|\tIf you happen to fight with a monster who is")
        print("|\tstronger than you. You'll lose.")
        print()
        print("Your command words are:")
        self.__parser.show_commands()

    """
     * Try to in to one direction. If there is an exit, enter the new
     * room, otherwise print an error message.
    """

    def go_room(self, command: Command):
        """Try to in to one direction. If there is an exit, enter the new
        room, otherwise print an error message.
        """
        if command.has_second_word() == False:
            # if there is no second word, we don't know where to go...
            print("Go where?")
            return

        direction = command.get_second_word()

        # Try to leave current room.
        next_room = self.__current_room.get_exit(direction)

        """ Ending point of the Game """
        if next_room == self.exit_room:
            if self.key:
                # You win
                print("\nFinally! You have found the exit. You win!")
                print("Thank you for playing. Good bye.\n")
                sys.exit()
            else:
                print("|\tYou need a Key to exit out of the Dungeon.")
                print("|\tCome back again.")

        monsters = self.get_monsters_in_room()
        if monsters:
            print("\nOops! You can't go anywhere, there is a monster in your room.")
            print("You must defeat the monster to pass through.")
            print("Or use 'back' command to go back to the room you came from.\n")
        else:
            self.go_next_room(next_room)

    def go_next_room(self, next_room):
        if (
            next_room == None
        ):  # None is a special Python value that says the variable contains nothing
            print("There is no door!")
        else:
            if next_room == self.magical_transporter_room:
                next_room = self.get_random_room()
                # Remove track of last room, because player was transported
                self.last_room = None
                # Tell the player that he was transported through magic
                print("------------------------------")
                print("You entered into the Magical Room.")
                print("Now you are being transported to a random room....")
            else:
                self.last_room = self.__current_room
            self.__current_room = next_room
            # Update the rooms of player and items
            self.player.change_room(next_room)

            print()
            print(self.__current_room.get_long_description())
            self.print_objects_in_current_room()

    def get_objects_in_room(self, room: Room) -> dict:
        """It will return all the objects in the current room"""
        objects = {"Monsters": [], "Weapons": [], "Items": []}
        for item in self.items:
            if item.get_room() is room:
                objects["Items"].append(item)

        for monster in self.monsters:
            if monster.get_room() is room:
                objects["Monsters"].append(monster)

        for weapon in self.weapons:
            if weapon.get_room() is room:
                objects["Weapons"].append(weapon)

        return objects

    def quit(self, command: Command):
        """ "Quit" was entered. Check the rest of the command to see whether we really quit the game.

        Parameters
        ----------
        command: Command
            The command to be processed

        Returns true, if this command quits the game, false otherwise.
        """
        if command.has_second_word():
            print("Quit what?")
            return False
        else:
            return True  # signal that we want to quit

    def get_random_room(self):
        """Returns a random room from the Map"""
        rooms = [
            v
            for k, v in self.map.rooms.items()
            if k not in [START_ROOM, EXIT_ROOM, self.magical_transporter_room]
        ]
        return choice(rooms)

    def play(self):
        """Main play routine.  Loops until end of play"""
        self.print_welcome()
        finished = False
        while finished == False:
            # Display all objects in current room
            command = self.__parser.get_command()
            finished = self.process_command(command)
        print("Thank you for playing.  Good bye.")

    def give_item(self, command: Command):
        if command.has_second_word() == False:
            # if there is no second word, we don't know give to whom...
            print("Give to whom?")
            return

        if command.has_third_word() == False:
            # if there is no third word, we don't know what to give...
            print("Give what?")
            return

        creature_name: str = command.get_second_word()
        item: str = command.get_third_word()

        if self.dwarf and self.dwarf.get_room() == self.__current_room:
            # The Dwarf is in current room
            monsters = self.get_monsters_in_room()
            if monsters:
                # There are monsters in this room as well
                # You can't save the creature unless you defeat
                # the monsters
                print(f"Defeat the monsters in this room to trade with {self.dwarf}")
            else:
                # Give item to Dwarf
                if creature_name == "dwarf":
                    self.give_item_to_dwarf(item)
                else:
                    print(f"{creature_name} is not in the room.")
        else:
            print("There is no Dwarf in this room.")

    def pick_item(self, command: Command):
        """A player can pick items from a room upto a certain weight.
        Item can either be food, herb"""
        if command.has_second_word() == False:
            # if there is no second word, we don't know what to pick...
            print("pick what?")
            return
        item_name = command.get_second_word()  # herb, food
        if item_name not in self.item_types + self.weapon_types:
            print("Item doesn't exist")
            return

        if item_name in self.weapon_types:
            self.pick_weapon(item_name)
            return

        # Valid item
        items = self.get_items_in_room()
        for item in items:
            if item.get_name().lower().split()[0] == item_name:
                # Item exists in current room
                monsters = self.get_monsters_in_room()
                if monsters:
                    print("You have to defeat the monster to pick the item.")
                    return
                else:
                    if item.weight > self.player.weight_of_items_left:
                        print(f"|\tYou cannot pick {item}.")
                        print(
                            f"|\tYou can only pick an item under {self.player.weight_of_items_left} pounds."
                        )
                        print()
                        return
                    # Pick item
                    self.player.pick_item(item)
                    # Remove item from map
                    self.items.remove(item)
                    print(f"{item} picked")

    def drop_item(self, command: Command):
        """A player can drop items from his inventory to save some space
        for other items. Item can either be food or herb"""
        if command.has_second_word() == False:
            # if there is no second word, we don't know what to drop...
            print("drop what?")
            return
        item_name = command.get_second_word()  # herb, food
        if item_name not in self.item_types + self.weapon_types:
            print("Item doesn't exist")
            return

        for item in chain(self.player.inventory, self.player.weapons):
            if item.get_name().lower().split()[0] == item_name:
                if item_name in self.item_types:
                    self.player.drop_item(item)
                    print(f"{item} was dropped.")
                    # Add the weapon back to the map
                    self.items.append(item)
                elif item_name in self.weapon_types:
                    self.player.drop_weapon(item)
                    print(f"{item} was dropped.")
                    # Add the weapon back to the map
                    self.weapons.append(item)
                else:
                    print("Invalid item.")
                # Break so that only one item can be dropped at a time
                break

    def pick_weapon(self, weapon_name):
        """A player can pick weapons from a room upto a certain weight.
        Weapon can either be Sword or Spear"""
        # Valid weapon
        weapons = self.get_weapons_in_room()
        for weapon in weapons:
            if weapon.get_name().lower().split()[0] == weapon_name:
                # Weapon exists in current room
                monsters = self.get_monsters_in_room()
                if monsters:
                    print("You have to defeat the monster to pick the weapon.")
                    return
                else:
                    if weapon.weight > self.player.weight_of_items_left:
                        print(
                            f"|\tYou cannot pick {weapon}. It's weight is {weapon.weight} pounds."
                        )
                        print(
                            f"|\tYou can only pick an weapon under {self.player.weight_of_items_left} pounds."
                        )
                        print()
                        return
                    # Pick weapon
                    self.player.pick_weapon(weapon)
                    # Remove weapon from map
                    self.weapons.remove(weapon)
                    print(f"{weapon} picked")

    def go_back(self):
        if self.last_room:
            self.go_next_room(self.last_room)
        else:
            print("You can't go back because you were transported here.")

    def get_monsters_in_room(self, room=None):
        if not room:
            room = self.__current_room
        return self.get_objects_in_room(room)["Monsters"]

    def get_items_in_room(self, room=None):
        if not room:
            room = self.__current_room
        return self.get_objects_in_room(room)["Items"]

    def get_weapons_in_room(self, room=None):
        if not room:
            room = self.__current_room
        return self.get_objects_in_room(room)["Weapons"]

    def fight(self):
        """Fight with all monsters in the current room
        with all the weapons the player has. When there is
        no weapon player fights barehanded and he may die.
        Does nothing if there is no monster in the room.
        """
        monsters = self.get_monsters_in_room()
        if monsters:
            # There are monsters in current room
            dead_monsters = []
            for monster in monsters:
                print()
                print(f"Let's fight with the {monster}")
                print("Bam Bam Bam!")
                try:
                    monster_died = self.player.fight(monster)
                except PlayerWeakerThanMonsterException as e:
                    # Print error description, user died against monster
                    print(e)
                    # Exit the program, game ended
                    sys.exit()
                if monster_died:
                    dead_monsters.append(monster)
                    print(f"You just defeated {monster}. Yay!")
                    print()

            # Remove dead monster from the map/game
            for dead_monster in dead_monsters:
                self.monsters.remove(dead_monster)
        else:
            # There is no monster in current room
            print("There is no monster in the room!")

    def give_item_to_dwarf(self, item):
        """Dwarf need either herbs or food"""
        if item == "herb":
            herb = self.player.get_herb()
            if herb:
                print("Giving herb to Dwarf")
                self.player.remove_herb(herb)
                # In return Dwarf gives you the key
                self.key = True
                self.dwarf = None
                print("Cool! Now you have the key of the exit.")
                print("Dwarf goes away....")
            else:
                print(f"You don't have herb to give to {self.dwarf}.")
        elif item == "food":
            food = self.player.get_food()
            if food:
                print("Giving food to Dwarf")
                self.player.remove_food(food)
                # In return Dwarf gives you the key
                self.key = True
                self.dwarf = None
                print("Cool! Now you have the key of the exit.")
                print("Dwarf goes away....")
            else:
                print(f"You don't have food to give to {self.dwarf}.")
        else:
            print("Invalid item. Item can be either food or herb")

    def status(self):
        """This function will print the status of the player"""
        print(
            f"You can pick items upto weight {self.player.weight_of_items_left} pounds"
        )
        print(f"- Health: {self.player.hp}")
        print("- Inventory:")
        for item in self.player.inventory:
            print(item)
        print("- Weapons:")
        for weapon in self.player.weapons:
            print(weapon, end=" HP: ")
            print(weapon.hp)
        if self.key:
            print("- The Key")

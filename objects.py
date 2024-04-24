from random import choice
from typing import List
from room import Room
from utils import PlayerWeakerThanMonsterException


class DungeonObject:
    """
    A DungeonObject is either an Animate Object or Inanimate Object
    used in the game as a base class for all other objects.
    It has:
        Name
        Description
        Room
    """

    def __init__(self, name: str, description: str, room: Room) -> None:
        self.__name = name
        self.__description = description
        self.__room = room

    def change_room(self, room: Room):
        self.__room = room

    def get_room(self):
        return self.__room

    def get_name(self):
        return self.__name

    def __str__(self) -> str:
        """Return the string representation of the DungeonObject"""
        return self.__name

    def get_description(self) -> str:
        """Return the description of the DungeonObject"""
        return self.__description


class Creature(DungeonObject):
    """
    A Creature or Animate Object can move through the rooms occasionally.
    """

    def __init__(self, name: str, description: str, room: Room) -> None:
        super().__init__(name, description, room)

    def move(self):
        """A Creature will move randomly in any direction from its
        current position after some interval"""
        exits: dict = self.__room.exits
        # Get all exits of the room in which the object is.
        possible_rooms = list(exits.values())
        # Select a random room from the exits
        random_room = choice(possible_rooms)
        # Change the current room of the object to new room
        self.change_room(random_room)


class Item(DungeonObject):
    """
    An Item has a weight and it cannot move on it's own.
    The player can pick and drop an item.
    """

    def __init__(self, name: str, description: str, room: Room, weight: int) -> None:
        super().__init__(name, description, room)
        self.__weight = weight

    @property
    def weight(self):
        return self.__weight

    def __str__(self) -> str:
        return f"{self.get_name()} ({self.weight} pounds)"


class Weapon(Item):
    """
    A Weapon can be used to fight against monsters.
    It can be either a sword, spear."""

    def __init__(
        self, name: str, description: str, room: Room, weight: int, hp: int
    ) -> None:
        super().__init__(name, description, room, weight)
        self.__hp = hp

    def decrease_hp(self, value):
        """A weapon may lose it's hp while fighting with a Monster"""
        self.__hp -= value
        if self.__hp <= 0:
            # Weapon should break
            pass

    @property
    def hp(self):
        return self.__hp

class Dwarf(Creature):
    """
    A Dwarf is not dangerous for the player.
    Player can do missions, provide items to Dwarf and
    in return they can get information of the dungeon like the map or
    the 'key' to the exit.
    """

    def __init__(self, name: str, description: str, room: Room) -> None:
        super().__init__(name, description, room)




class Monster(Creature):
    """
    A Monster is dangerous for the player.
    Monster will attack on the player as soon they encounter each other.
    Monster can be defeated with Weapon like sword, magical items or shield.
    If a Player defeats a Monster and save a Dwarf, he can get
    information or the 'key' to the exit.
    """

    def __init__(self, name: str, description: str, room: Room, hp: int) -> None:
        """
        Name
        Description
        Room
        HP (Hit Points)
        """
        super().__init__(name, description, room)
        self.__hp = hp

    def deplete_hp(self, value):
        self.__hp -= value

    @property
    def hp(self) -> int:
        return self.__hp


class Player:
    """Player is the user of the program.
    Player can:
        travel into different room
        pick items, drop items,
        give items to Dwarf
        fight Monster
    Player has:
        HP, Inventory, Room
    """

    def __init__(self, hp) -> None:
        self.__room: Room = None
        self.__inventory: List[Item] = []
        self.__weapons: List[Weapon] = []
        self.__hp = hp
        self.__weight_of_items_left = 200

    def increase_hp(self, value: int):
        self.__hp += value

    def decrease_hp(self, value: int):
        self.__hp -= value

    def pick_item(self, item: Item):
        self.__weight_of_items_left -= item.weight
        self.__inventory.append(item)

    def drop_item(self, item: Item):
        self.__weight_of_items_left += item.weight
        self.__inventory.remove(item)

    def pick_weapon(self, weapon: Weapon):
        self.__weight_of_items_left -= weapon.weight
        self.__weapons.append(weapon)

    def drop_weapon(self, weapon: Weapon):
        self.__weight_of_items_left += weapon.weight
        self.__weapons.remove(weapon)

    def change_room(self, room: Room):
        for item in self.__inventory:
            item.change_room(room)
        for weapon in self.__weapons:
            weapon.change_room(room)
        self.__room = room

    def get_herb(self):
        for item in self.__inventory:
            if item.get_name().lower().split()[0] == "herb":
                # item is HERB
                return item

    def get_food(self) -> Item:
        for item in self.__inventory:
            if item.get_name().lower().split()[0] == "food":
                # item is food
                return item

    def remove_food(self, food):
        self.__weight_of_items_left += food.weight
        self.__inventory.remove(food)

    def remove_herb(self, herb):
        self.__inventory.remove(herb)

    @property
    def inventory(self):
        return self.__inventory

    @property
    def weapons(self):
        return self.__weapons

    @property
    def hp(self):
        return self.__hp

    @property
    def weight_of_items_left(self) -> int:
        return self.__weight_of_items_left

    def fight(self, monster: Monster):
        """Fight with monster using weapons
        Returns True if monster dies otherwise return False"""
        broken_weapons = []  # Keep track of broken weapons
        monster_died = False
        # Use all weapons in arsenal to fight against the monster
        for weapon in self.__weapons:
            player_won = attack(weapon, monster)
            if player_won:
                # Monster died
                monster_died = True
                if weapon.hp <= 0:
                    # Weapon also broke
                    broken_weapons.append(weapon)
                break
            else:
                # Weapon broke
                broken_weapons.append(weapon)

        for broken_weapon in broken_weapons:
            # Remove broken weapon from player's arsenal
            # Remove weapon weight from player
            self.drop_weapon(broken_weapon)

        # If the player doesn't have a weapon
        # He will fight with his own hands and he may die
        if not self.__weapons:
            player_won = attack(self, monster)
            if player_won:
                # Monster died
                monster_died = True
            else:
                # If player died, raise exception and player loses
                raise PlayerWeakerThanMonsterException("Player Died! You lose.")

        return monster_died


def attack(obj, monster: "Monster") -> bool:
    """For simplicity we'll only look for Monster's hp
    and Object's hp. (Object maybe `Weapon` or `Player`)

    This attack method is called when the Player decides to
    fight with the monster

    Returns True if weapon wins against monster else return False"""
    if monster.hp > obj.hp:
        # Monster is more powerful than our Object
        # Object will break
        # Monster will get hurt
        monster.deplete_hp(obj.hp)
        return False
    # Our Object is stronger than the Monster
    # Monster will die
    # Object will lose it's hp
    obj.decrease_hp(monster.hp)
    return True

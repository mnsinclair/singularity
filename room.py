from __future__ import annotations
import numpy as np
from action import Action
from typing import List, Set
import person


class Room:
    def __init__(self, name: str):
        assert(type(name) == str), f"{name} is not a string"

        self.__name = name  # The name of the room
        self.__people = set()  # The set of people currently in the room
        # The set of rooms that are adjacent to this room. Empty to start with.
        self.__adjacent_rooms = set()

    def __repr__(self):
        return f"""
        ===========================
        The {self.__name}:
        ===========================
        People: {[str(x) for x in self.__people]}
        Num people: {len(self.__people)}
        Adjacent to: {self.get_adjacent_room_names()}
        """

    def is_someone_free_to_chat(self):
        """Returns true if someone is free to chat in this room"""
        for person in self.__people:
            if not person.has_conversation_partner():
                return True
        else:
            return False

    def get_name(self):
        """Returns room name"""
        return self.__name

    def add_person(self, person_to_add):
        """Adds a person to the room"""
        assert(
            person_to_add not in self.__people), f"{person_to_add} is already in {self.__name}"
        assert(type(person_to_add) ==
               person.Person), f"{person_to_add} is not a person"
        self.__people.add(person_to_add)

    def remove_person(self, person_to_add):
        """Removes a person from the room"""
        assert(
            person_to_add in self.__people), f"{person_to_add} is not in {self.__name}"
        self.__people.remove(person_to_add)

    def has_person(self, person):
        """Returns true if the person is in the room"""
        return person in self.__people

    def get_people(self):
        """Returns the people in the room"""
        return self.__people

    def get_adjacent_rooms(self):
        """Returns the adjacent rooms to this room"""
        return self.__adjacent_rooms

    def get_adjacent_room_names(self):
        """Returns the names of the adjacent rooms"""
        return [x.get_name() for x in self.get_adjacent_rooms()]

    def add_adjacent_room(self, other_room):
        """Adds an adjacent room to this room"""
        assert(type(other_room) == Room), f"{other_room} is not a room"
        assert(
            other_room not in self.__adjacent_rooms), f"{other_room} is already adjacent to {self.__name}"
        # Add an adjacent room to the set of adjacent rooms
        self.__adjacent_rooms.add(other_room)

        if self not in other_room.get_adjacent_rooms():
            # Add this room to the set of adjacent rooms of the other room
            other_room.add_adjacent_room(self)

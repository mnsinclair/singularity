from __future__ import annotations
import numpy as np
from action import Action
from typing import List, Set
import person


class Room:
    def __init__(self, name: str, adjacent_rooms: Set[Room] = set(), people_in_room: Set[person.Person] = set()):
        assert(type(name) == str), f"{name} is not a string"
        assert(np.array([type(room) == Room for room in adjacent_rooms]).all(
        )), f"{adjacent_rooms} is not a set of rooms"
        assert(np.array([type(person) == person.Person for person in people_in_room]).all(
        )), f"{adjacent_rooms} is not a set of people"

        self.__name = name  # The name of the room
        self.__people = set()  # The set of people currently in the room
        # The set of rooms that are adjacent to this room. Empty to start with.
        self.__adjacent_rooms = adjacent_rooms

    def __repr__(self):
        return f"""
        ===========================
        The {self.__name}:
        ===========================
        People: {[str(x) for x in self.__people]}
        Num people: {len(self.__people)}
        Adjacent to: {self.get_adjacent_room_names()}
        """

    def get_name(self):
        """Returns room name"""
        return self.__name

    def add_person(self, person):
        """Adds a person to the room"""
        assert(
            person not in self.__people), f"{person} is already in {self.__name}"
        assert(type(person) == person.Person), f"{person} is not a person"
        self.__people.add(person)

    def remove_person(self, person):
        self.__people.remove(person)

    def has_person(self, person):
        return person in self.__people

    def get_people(self):
        return self.__people

    def get_adjacent_rooms(self):
        # Get the adjacent rooms to this one
        return self.__adjacent_rooms

    def get_adjacent_room_names(self):
        return [x.get_name() for x in self.get_adjacent_rooms()]

    def add_adjacent_room(self, other_room):
        """Adds an adjacent room to this room"""
        assert(type(other_room) == Room), f"{other_room} is not a room"
        assert(
            other_room not in self.__adjacent_rooms), f"{other_room} is already adjacent to {self.__name}"
        # Add an adjacent room to the set of adjacent rooms
        self.__adjacent_rooms.add(other_room)
        # Adjacency is reflexive (if A is adjacent to B, then B is adjacent to A)
        if self not in other_room.get_adjacent_rooms():
            other_room.add_adjacent_room(self)

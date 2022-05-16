class Room:
    def __init__(self, name, base_loudness=0, intended_occupancy=5, has_food=False, has_drinks=False):
        self.name = name  # The name of the room
        self.people = set()  # The set of people currently in the room
        # How loud the room is with no-one in it. 0 is silent.
        self.base_loudness = base_loudness
        # How many people can comfortably fit in the room before it is crowded.
        self.intended_occupancy = intended_occupancy
        # Whether the room has food available
        self.has_food = has_food
        # Whether the room has food available
        self.has_drinks = has_drinks
        # The set of rooms that are adjacent to this room. Empty to start with.
        self.adjacent_rooms = set()

    def add_adjacent_room(self, room):
        # Add an adjacent room to the set of adjacent rooms
        self.adjacent_rooms.add(room)
        # Adjacency is reflexive (if A is adjacent to B, then B is adjacent to A)
        if self not in room.get_adjacent_rooms():
            room.add_adjacent_room(self)

    def get_people(self):
        return self.people

    def get_adjacent_rooms(self):
        # Get the adjacent rooms to this one
        return self.adjacent_rooms

    def get_adjacent_room_names(self):
        return [x.get_name() for x in self.get_adjacent_rooms()]

    def get_current_loudness(self):
        # Todo define the relationship between people & loudness (maybe speaking volume attribute in the Person class)
        return self.base_loudness + len(self.people)

    def get_current_crowdedness(self):
        # Todo define the relationship between number of people & how crowded the room feels (maybe speaking volume attribute in the Person class)
        if self.intended_occupancy == 0:
            # Avoid a divide by zero error
            return float("inf")
        return len(self.people) / self.intended_occupancy * 100

    def __repr__(self):
        return f"""
        ===========================
        The {self.name}:
        ===========================
        People: {[str(x) for x in self.people]}
        Num people: {len(self.people)}
        Base Loudness: {self.base_loudness}
        Current Loudness: {self.get_current_loudness()}
        Intended Capacity: {self.intended_occupancy}
        Crowdedness (% max capacity): {self.get_current_crowdedness()}
        Has food: {self.has_food}
        Has drinks: {self.has_drinks}
        Adjacent to: {self.get_adjacent_room_names()}
        """

    def get_name(self):
        return self.name

    def add_person(self, person):
        self.people.add(person)

    def remove_person(self, person):
        self.people.remove(person)

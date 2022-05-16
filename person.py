import numpy as np
from action import Action


class Person:
    def __init__(self, name, location_state, personality_scales=None, emotional_state=None, social_state=None):
        self.name = name

        self.action_type_probs = {"verbal": 1/3,
                                  "non-verbal": 1/3, "move": 1/3}
        self.personality_scales = personality_scales if personality_scales != None else {
            "openness": 1,
            "conscientiousness": 1,
            "extraversion": 1,
            "agreeableness": 1,
            "neuroticism": 1
        }
        # PAD model of emotions
        self.emotional_state = emotional_state if emotional_state != None else {
            "pleasure_displeasure": 0,
            "arousal_nonarousal": 0,
            "dominance_submissiveness": 0
        }
        self.social_state = social_state if social_state != None else dict()

        # Initialise the location state to the given location, otherwise
        self.location_state = location_state
        # Add self to the collection of people in the room
        self.location_state.add_person(self)

    def __repr__(self):
        return self.name

    def take_action(self, type=None):
        """This funciton selects the action to take next and returns it."""
        # If no type of action is specified, select one.
        if type == None:
            type = self.select_action_type()

        if type == "verbal":
            verbal_action = self.select_verbal_action()
            return verbal_action

        elif type == "non-verbal":
            non_verbal_action = self.select_non_verbal_action()
            return non_verbal_action

        elif type == "move":
            to_room = self.select_next_room()
            return self.move_to(to_room)

        else:
            print(type)

    def select_non_verbal_action(self):
        # TODO implement non-verbal action selection. This could use any of the below attributes. For now, just return an empty action.
        # self.personality_scales
        # self.social_state
        # self.emotional_state
        # self.location_state (Any of the properties of the location state (current room) can be used to influence the action taken.)
        return Action(name="DefaultNonVerbalAction", taker=self, description="takes a non verbal action")

    def select_verbal_action(self):
        # TODO implement verbal action. This could use any of the below attributes. For now, just return a default action.
        # self.personality_scales
        # self.social_state
        # self.emotional_state
        # self.location_state (Any of the properties of the location state (current room) can be used to influence the action taken.)
        return Action(name="DefaultVerbalAction", taker=self, description="takes a verbal action")

    def select_next_room(self):
        # TODO implement how next room is selected. Could include things like people in room, whether food available etc. For now, just pick a random adjacent room.
        ajacent_rooms = self.location_state.get_adjacent_rooms()
        return np.random.choice(list(ajacent_rooms))

    def move_to(self, room):
        from_room = self.location_state
        to_room = room
        # Remove self from the current room
        from_room.remove_person(self)
        # Update own location state to the new room
        self.location_state = to_room
        # Add self to the new room 'people set'
        to_room.add_person(self)

        return Action(name="movement", taker=self, description=f"leaves the {from_room.get_name()} and enters the {to_room.get_name()}")

    def select_action_type(self):
        # TODO implement a function to select what type of action to take next. For now, just select a random action type.
        action_types = list(self.action_type_probs.keys())
        action_probs = list(self.action_type_probs.values())
        return np.random.choice(action_types, p=action_probs)

import numpy as np
from action import Action
from typing import List
from room import Room
# Allows type hint to have Person class (get_conversation_partner())
from __future__ import annotations


class Person:
    def __init__(self, name, location_state, personality_scales=None, emotional_state=None, social_state=None):
        self.name = name

        self.action_type_probs = {"verbal": 1/3,
                                  "non-verbal": 1/3, "move": 1/3}
        self.personality_scales = personality_scales if personality_scales != None else {
            "openness": 0,
            "conscientiousness": 0,
            "extraversion": 0,
            "agreeableness": 0,
            "neuroticism": 0
        }
        # PAD model of emotions
        self.emotional_state = emotional_state if emotional_state != None else {
            "pleasure_displeasure": 0,
            "arousal_nonarousal": 0,
            "dominance_submissiveness": 0
        }
        self.social_state = social_state if social_state != None else dict()

        self.base_action_probs = self.get_base_action_probs(
            self.personality_scales)

        # Initialise the location state to the given location, otherwise
        self.location_state = location_state
        # Add self to the collection of people in the room
        self.location_state.add_person(self)

    def __repr__(self):
        return self.name

    def get_base_action_probs(self, personality):
        pass

    def get_emotional_action_probs(self, pad):
        pass

    def filter_probs(self, probs_dict, available_conv_act, available_room_act):
        filtered_probs = dict()
        total_sum = 0
        # eliminate invalid actions
        for action in available_conv_act:
            filtered_probs[action] = probs_dict[action]
            total_sum += probs_dict[action]

        for action in available_room_act:
            filtered_probs[action] = probs_dict[action]
            total_sum += probs_dict[action]

        filtered_probs = {action: prob/total_sum for action,
                          prob in filtered_probs.items()}

        return filtered_probs

    def combine_emotion_base_probs(self, emotion_probs, base_probs, weighting=0.5):
        combined_probs = dict()
        for key in emotion_probs.keys():
            combined_probs[key] = (
                emotion_probs[key] * weighting + base_probs[key] / (1 + weighting))
        return combined_probs

    def action_selection(self, available_conv_act, available_room_act):
        # Get action probabilities based on persons emotional state
        emotional_action_probs = self.get_emotional_action_probs(
            self.emotional_state)
        # remove invalid actions from selection
        filtered_emotional_probs = self.filter_probs(
            emotional_action_probs, available_conv_act, available_room_act)
        filtered_base_probs = self.filter_probs(
            self.base_action_probs, available_conv_act, available_room_act)

        combined_probs = self.combine_emotion_base_probs(
            filtered_emotional_probs, filtered_base_probs)
        action = np.random.choice(
            combined_probs.keys(), p=combined_probs.values())

        return action

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

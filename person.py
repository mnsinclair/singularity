# Allows type hint to have Person class (get_conversation_partner())
from __future__ import annotations
import numpy as np
from action import Action
from typing import List
import room


class Person:
    def __init__(self, name: str, location_state: room.Room, personality_vector: np.array | None = None, emotional_state_vector: np.array | None = None, conversation_partner: Person | None = None, all_possible_actions: List[Action] = None):
        # Initialize the person's name
        self.__name = name

        # Personality (Modelled by the "Big 5" personality scales).
        # OCEAN: openness, conscientiousness, extraversion, agreeableness, neuroticism
        # Personality is expressed as a 5 dimensional vector, on a scale from 1 to -1.
        # Dimensions are (in this order):
        # Openness: open to new experiences, curious (1 is highly open)
        # Conscientiousness: responsible, self-disciplined (1 is highly conscientious)
        # Extraversion: energetic, sociable, talkative (1 is highly extraverted)
        # Agreeableness: cooperative, pleasant with others, sociable (1 is highly agreeable)
        # Neuroticism: nervous, anxious, suspicious (1 is highly neurotic)
        self.__personality_vector = personality_vector if personality_vector else np.zeros(
            5)

        # Person's current emotional state (Modelled by the "PAD" emotional model)
        # PAD: Pleasure, Arousal, Dominance
        # Emotional state is expressed as a 3 dimensional vector, on a scale from 1 to -1.
        # Dimensions are (in this order):
        # Pleasure: how much one is happy (1 is highly happy)
        # Arousal: how much one is excited (1 is highly excited)
        # Dominance: how much one is dominant (1 is highly dominant)
        self.__emotional_state_vector = emotional_state_vector if emotional_state_vector else np.zeros(
            3)

        # The base action probabilities are derived solely from personality.
        # This means they are static, and do not change over time.
        # N.B. These probabilities are analagous to the emotional_action_probs,
        # but those must be derived for the current emotional state, which changes over time.
        self.__base_action_probs = None
        self.set_base_action_probs()

        # Initialise the location state to the given location
        self.__location_state = location_state
        # Add self to the collection of people in the room
        self.__location_state.add_person(self)

        # Initialise the conversation partner
        self.__conversation_partner = conversation_partner

        # Initialise the all possible actions
        self.__all_possible_actions = all_possible_actions

    def __repr__(self) -> str:
        return self.__name

    def get_name(self) -> str:
        """Returns the name of the person"""
        return self.__name

    def get_personality_vector(self) -> np.array:
        """Returns the personality vector of the person"""
        return self.__personality_vector

    def get_emotional_state_vector(self) -> np.array:
        """Returns the emotional state vector of the person"""
        return self.__emotional_state_vector

    def set_emotional_state_vector(self, emotional_state_vector: np.array):
        """Sets the emotional state vector of the person"""
        assert(type(emotional_state_vector) ==
               np.ndarray), "Emotional state vector must be a numpy array"
        assert(len(emotional_state_vector) ==
               3), "Emotional state vector must be 3 dimensional"
        assert(np.all(emotional_state_vector >= -1) and np.all(emotional_state_vector <= 1)
               ), "Emotional state vector values must be between -1 and 1"
        self.__emotional_state_vector = emotional_state_vector

    def get_base_action_probs(self) -> dict:
        """Returns the base action probabilities"""
        # Initialise an empty dictionary
        base_action_probs = dict()
        # Loop through all possible actions
        for action in self.__all_possible_actions:
            # Get the "most likely personality" for the action
            most_likely_personality_vector = action.get_most_likely_personality_vector()
            # Compute the distance between this person's personality and the most likely personality
            personality_distance = np.linalg.norm(
                self.__personality_vector - most_likely_personality_vector)
            # We want the probability to be inversely proportional to the distance.
            # That is, the more closely this personality aligns with the "most likely personality" for the action
            # The more likely this person is to take that action.
            base_action_probs[action] = 1 / personality_distance
        # Normalise the action probabilities to sum to 1
        base_action_probs = self.normalise_action_probs(base_action_probs)
        return base_action_probs

    def set_base_action_probs(self) -> dict:
        """This function returns the "base action probabilities" for the person, derived solely from the "personality" attribute."""
        assert(self.__base_action_probs ==
               None), "Base action probabilities already set"
        pass

    def get_location_state(self) -> room.Room:
        """Returns location state"""
        return self.__location_state

    def set_location_state(self, location_state: room.Room):
        """Sets the location state of the person"""
        assert self.__location_state != location_state, "Already in this location"
        assert self.__conversation_partner == None, "Cannot change location while in conversation"
        self.__location_state = location_state

    def has_conversation_partner(self) -> bool:
        return self.__conversation_partner != None

    def get_conversation_partner(self) -> Person | None:
        return self.__conversation_partner

    def set_conversation_partner(self, partner):
        assert(self.__conversation_partner ==
               None), "Already in a conversation"
        assert(partner.conversation_partner ==
               None), "Partner already in a conversation"
        assert(self.__location_state ==
               partner.location_state), "Partner not in same location"
        assert(self.__name != partner.name), "Cannot have conversation with self"

        self.__conversation_partner = partner

    def get_emotional_action_probs(self) -> dict:
        """This function returns the "emotional action probabilities" for the person, 
        derived solely from the "emotional_state_vector" attribute."""

        # Initialise an empty dictionary
        emotional_action_probs = dict()
        # Loop through all possible actions
        for action in self.__all_possible_actions:
            # Get the "most likely emotional state" for the action
            most_likely_emotional_vector = action.get_most_likely_emotional_vector()
            # Compute the distance between this person's emotional state and the most likely emotional state
            emotional_state_distance = np.linalg.norm(
                self.__emotional_state_vector - most_likely_emotional_vector)
            # We want the probability to be inversely proportional to the distance.
            # That is, the more closely this person's emotional state aligns with the "most likely emotional state" for the action
            # The more likely this person is to take that action.
            emotional_action_probs[action] = 1 / emotional_state_distance
        # Normalise the action probabilities to sum to 1
        emotional_action_probs = self.normalise_action_probs(
            emotional_action_probs)
        return emotional_action_probs

    def normalise_action_probs(self, probs: dict) -> dict:
        total_sum = sum(probs.values())
        # Normalise the relevant probabilities so they sum to 1
        return {action: likelihood/total_sum for action, likelihood in probs.items()}

    def filter_action_probs(self, probs_dict: dict, available_conv_act: List[Action] = [], available_room_act: List[Action] = []) -> dict:
        """This function filters out the invalid actions from ALL action probabilities."""
        filtered_probs = dict()
        total_sum = 0
        # add only actions in available_conv_act
        for action in available_conv_act:
            filtered_probs[action] = probs_dict[action]
            total_sum += probs_dict[action]

        # add only actions in available_room_act
        for action in available_room_act:
            filtered_probs[action] = probs_dict[action]
            total_sum += probs_dict[action]

        filtered_probs = self.normalise_action_probs(filtered_probs)

        return filtered_probs

    def combine_emotion_base_probs(self, emotion_probs: dict, base_probs: dict, weighting: float = 0.5) -> dict:
        """This function combines the emotional action probabilities with the base action probabilities, and returns the result as a dictionary"""
        assert weighting >= 0 and weighting <= 1, "weighting must be between 0 and 1"
        assert emotion_probs.keys() == base_probs.keys(
        ), "Emotion and base action probabilities must have the same actions as keys"

        combined_probs = dict()
        for key in emotion_probs.keys():
            combined_probs[key] = (
                emotion_probs[key] * weighting + base_probs[key] / (1 + weighting))
        return combined_probs

    def action_selection(self, available_conv_act: List[Action], available_room_act: List[Action]) -> Action:
        """This function selects an action from the given available actions."""
        # Get action probabilities for ALL actions, based on persons current emotional state
        emotional_action_probs = self.get_emotional_action_probs(
            self.__emotional_state_vector)

        # filter to get the (emotional and base) distribution for only AVAILABLE actions.
        filtered_emotional_probs = self.filter_probs(
            emotional_action_probs, available_conv_act, available_room_act)
        filtered_base_probs = self.filter_probs(
            self.__base_action_probs, available_conv_act, available_room_act)

        # combine the two distributions
        combined_probs = self.combine_emotion_base_probs(
            filtered_emotional_probs, filtered_base_probs)
        action = np.random.choice(
            combined_probs.keys(), p=combined_probs.values())

        return action

    # Method to handle updating emotional_state_vector (for both own action, and partner's action)
    def update_emotional_state_vector(self, action: Action, isOwnAction: bool):
        if isOwnAction:
            # update own emotional state vector
            pass
        else:
            # update partner's emotional state vector
            pass
        pass

    # Methods to handle special non-conversation actions
    def leave_conversation(self):
        """This function handles the special case of a person leaving a conversation."""
        assert self.__conversation_partner != None, "No conversation partner to leave"
        if self.__conversation_partner.has_conversation_partner():
            self.__conversation_partner.leave_conversation()
        self.__conversation_partner = None

    def move_to_room(self, room):
        """This function handles the special case of a person moving to a new room."""
        from_room = self.get_location_state()
        to_room = room
        # Remove self from the current room
        from_room.remove_person(self)
        # Update own location state to the new room
        self.set_location_state(to_room)
        # Add self to the new room 'people set'
        to_room.add_person(self)

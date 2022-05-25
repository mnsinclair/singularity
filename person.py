# Allows type hint to have Person class (get_conversation_partner())
from __future__ import annotations
import numpy as np
from action import Action
from typing import List
from room import Room


class Person:
    def __init__(self, name: str, location_state: Room, personality_vector: np.array | None = None, emotional_state_vector: np.array | None = None, conversation_partner: Person | None = None):
        # Initialize the person's name
        self.name = name

        # Personality (Modelled by the "Big 5" personality scales).
        # OCEAN: openness, conscientiousness, extraversion, agreeableness, neuroticism
        # Personality is expressed as a 5 dimensional vector, on a scale from 1 to -1.
        # Dimensions are (in this order):
        # Openness: open to new experiences, curious (1 is highly open)
        # Conscientiousness: responsible, self-disciplined (1 is highly conscientious)
        # Extraversion: energetic, sociable, talkative (1 is highly extraverted)
        # Agreeableness: cooperative, pleasant with others, sociable (1 is highly agreeable)
        # Neuroticism: nervous, anxious, suspicious (1 is highly neurotic)
        self.personality_vector = personality_vector if personality_vector else np.zeros(
            5)

        # Person's current emotional state (Modelled by the "PAD" emotional model)
        # PAD: Pleasure, Arousal, Dominance
        # Emotional state is expressed as a 3 dimensional vector, on a scale from 1 to -1.
        # Dimensions are (in this order):
        # Pleasure: how much one is happy (1 is highly happy)
        # Arousal: how much one is excited (1 is highly excited)
        # Dominance: how much one is dominant (1 is highly dominant)
        self.emotional_state_vector = emotional_state_vector if emotional_state_vector else np.zeros(
            3)

        # The base action probabilities are derived solely from personality.
        # This means they are static, and do not change over time.
        # N.B. These probabilities are analagous to the emotional_action_probs,
        # but those must be derived for the current emotional state, which changes over time.
        self.base_action_probs = self.get_base_action_probs(
            self.personality_scales)

        # Initialise the location state to the given location
        self.location_state = location_state
        # Add self to the collection of people in the room
        self.location_state.add_person(self)

        # Initialise the conversation partner
        self.conversation_partner = conversation_partner

    def __repr__(self) -> str:
        return self.name

    def has_conversation_partner(self) -> bool:
        return self.conversation_partner != None

    def get_conversation_partner(self) -> Person | None:
        return self.conversation_partner

    def set_conversation_partner(self, partner):
        assert(self.conversation_partner == None), "Already in a conversation"
        assert(partner.conversation_partner ==
               None), "Partner already in a conversation"
        assert(self.location_state ==
               partner.location_state), "Partner not in same location"
        assert(self.name != partner.name), "Cannot have conversation with self"

        self.conversation_partner = partner

    def get_location_state(self) -> Room:
        """Returns location state"""
        return self.location_state

    def set_location_state(self, location_state: Room):
        """Sets the location state of the person"""
        assert self.location_state != location_state, "Already in this location"
        assert self.conversation_partner == None, "Cannot change location while in conversation"
        self.location_state = location_state

    def get_base_action_probs(self) -> dict:
        """This function returns the "base action probabilities" for the person, 
        derived solely from the "personality" attribute.

        This encodes the effect of personality on the action taken.

        Args:
            None
        Returns:
            A dictionary of action types as keys and their probabilities as values.
        """
        pass

    def get_emotional_action_probs(self) -> dict:
        """This function returns the "emotional action probabilities" for the person, 
        derived solely from the "emotional_state" attribute.

        Args:
            None
        Returns:
            A dictionary of action types as keys and their probabilities as values.
        """
        pass

    def filter_probs(self, probs_dict: dict, available_conv_act: List[Action] = [], available_room_act: List[Action] = []) -> dict:
        """This function filters out the invalid actions from the given action probabilities."""
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

        # Normalise the relevant probabilities so they sum to 1
        filtered_probs = {action: prob/total_sum for action,
                          prob in filtered_probs.items()}

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
            self.emotional_state)

        # filter to get the (emotional and base) distribution for only AVAILABLE actions.
        filtered_emotional_probs = self.filter_probs(
            emotional_action_probs, available_conv_act, available_room_act)
        filtered_base_probs = self.filter_probs(
            self.base_action_probs, available_conv_act, available_room_act)

        # combine the two distributions
        combined_probs = self.combine_emotion_base_probs(
            filtered_emotional_probs, filtered_base_probs)
        action = np.random.choice(
            combined_probs.keys(), p=combined_probs.values())

        return action

    # Methods to handle special non-conversation actions
    def leave_conversation(self):
        """This function handles the special case of a person leaving a conversation."""
        assert self.conversation_partner != None, "No conversation partner to leave"
        if self.conversation_partner.has_conversation_partner():
            self.conversation_partner.leave_conversation()
        self.conversation_partner = None

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

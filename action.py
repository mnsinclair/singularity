from __future__ import annotations
import numpy as np


class Action:
    def __init__(self, name: str, action_type: str, most_likely_emotional_vector: np.array | None = None, most_likely_personality_vector: np.array | None = None, received_emotional_change_vector: np.array | None = None, given_emotional_change_vector: np.array | None = None):
        self.__name = name  # The name of the action
        # The PAD vector that the action most closely matches
        self.__most_likely_emotional_vector = most_likely_emotional_vector if most_likely_emotional_vector else np.zeros(3)
        # The Personality vector that most closely matches the action
        self.__most_likely_personality_vector = most_likely_personality_vector if most_likely_personality_vector else np.zeros(5)
        # The Personality vector that shows how the Person is who is receiving
        # the action will be affected by this action
        self.__received_emotional_change_vector = received_emotional_change_vector if received_emotional_change_vector else np.zeros(3)
        # The Personality vector that shows how the Person is who is taking the action
        # will be affected by this action
        self.__given_emotional_change_vector = given_emotional_change_vector if given_emotional_change_vector else np.zeros(3)
        # The type of action i.e. conversation or room
        self.__action_type = action_type

    def __str__(self) -> str:
        return f"""
        ===========================
        Name: {self.__name}
        Type of action: {self.__action_type}
        Emotional Vector for the action: {self.__most_likely_emotional_vector}
        Personality Vector for the action: {self.__most_likely_personality_vector}
        Emotional Change Vector for the action taken by Partner: {self.__received_emotional_change_vector}
        Emotional Change Vector for the action taken by Self: {self.__given_emotional_change_vector}
        """

    def __repr__(self) -> str:
        return self.__name

    def get_name(self) -> str:
        """Returns the name of the action"""
        return self.__name

    def get_action_type(self) -> str:
        """Returns the type of action"""
        return self.__action_type

    def get_most_likely_emotional_vector(self) -> np.array:
        """Returns the Emotional vector(PAD) for an action"""
        return self.__most_likely_emotional_vector

    def get_most_likely_personality_vector(self) -> np.array:
        """Returns the Personality (Big 5) vector for an action"""
        return self.__most_likely_personality_vector

    def get_received_emotional_change_vector(self) -> np.array:
        """Returns the changes in Emotional vector(PAD) for an action taken by the conversation partner"""
        return self.__received_emotional_change_vector

    def get_given_emotional_change_vector(self) -> np.array:
        """Returns the changes in Emotional vector(PAD) for an action taken by self"""
        return self.__given_emotional_change_vector

import numpy as np
import pandas as pd
from action import Action
from person import Person

import os


def parse_vector(string_vector_iterable: pd.Series) -> pd.Series:
    """
    Parses a pd.Series of vectors in string representation (of form "[x,..,y,z]") into a pd.Series of numpy array objects
    """
    parsed_vectors = []
    for vector in string_vector_iterable:
        # If this vector is empty, skip it.
        if type(vector) != str:
            continue
        else:
            vector = vector[1:-1].split(',')
            vector = np.array([float(val.strip()) for val in vector])
            parsed_vectors.append(vector)
    return pd.Series(parsed_vectors)


def initialise_all_actions(action_filepath="action_values.csv"):
    """This function reads in action initialisation data & returns a np.array of Action objects"""
    actions_df = pd.read_csv(action_filepath)
    for col_name in actions_df.columns:
        if col_name == "action_name" or col_name == "action_type":
            continue
        else:
            actions_df[col_name] = parse_vector(actions_df[col_name])

    actions_initialised = []
    for _, action in actions_df.iterrows():
        # initialises action
        # Use kwargs to pass in the values of the action
        actions_initialised.append(Action(**action))

    return np.array(actions_initialised)


def get_names(filepath="names.csv"):
    return pd.read_csv(filepath, header=None).squeeze("columns")


def get_personality_vector(personality_number):
    personality_seed = personality_number % 32
    personality_vector_string = bin(personality_seed)[2:]
       
    personality_vector_string = "0" * \
        (5 - len(personality_vector_string)) + personality_vector_string
    intlist = []
    for char in personality_vector_string:
        if char == "0":
            intlist.append(-1)
        elif char == '1':
            intlist.append(1)


    return np.array(intlist)


def initialise_all_people(all_possible_actions, rooms, num_people=32):
    all_people = []
    # TODO get_names() should depend on num_people.
    names = get_names()
    for personality_number in range(num_people):
        personality_vector = get_personality_vector(personality_number)
        initial_emotional_state_vector = np.random.uniform(
            low=-1, high=1, size=3)
        initial_location_state = np.random.choice(rooms)
        new_person = Person(name=names[personality_number], location_state=initial_location_state, all_possible_actions=all_possible_actions,
                            personality_vector=personality_vector, emotional_state_vector=initial_emotional_state_vector, conversation_partner=None)
        all_people.append(new_person)
    return all_people

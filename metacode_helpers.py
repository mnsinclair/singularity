import numpy as np
import pandas as pd
from action import Action

#import names
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


def get_names(filepath="names.csv", num_names=32):
    if filepath in os.listdir():
        names = pd.read_csv(filepath, header=None).squeeze("columns")
    else:
        names = pd.Series([names.get_first_name() for _ in range(num_names)])
        names.to_csv("names.csv", index=None, header=None)
    return names

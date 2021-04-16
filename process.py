"""
Program main
===============================
This is the main file of my project, whose methods are
responsible for reading in/extracting/filtering data
from the dataset and generating trees and dictionaries.
===============================
This file is Copyright (c) 2020 Aditya Mehrotra.
"""
import pprint

from typing import List, Any, Optional, Tuple, Dict
import pandas as pd
import numpy as np
from bst import BinarySearchTree
from decision_tree import DecisionTree


def read_data() -> pd.DataFrame:
    """
    This function reads in my CSV and returns a pandas
    dataframe

    :return:
        Pandas dataframe
    """
    df = pd.read_csv("data/pokemon.csv")
    return df


def find_quantiles(df: pd.DataFrame) -> Dict[str, Tuple[Optional[float], Optional[float]]]:
    """
    This function generates a dictionary which maps
    degrees into tuples in the form (Lower bound, Upper bound)
    where Upper bound or lower bound is None if there is no upper bound or lower bound

    Please see the project report for more information
    :param df:
        a pandas dataframe
    :return:
        A dictionary degree to contraints mapping
    """
    stat_to_quantiles = {}
    stats = ["attack", "defense", "speed", "sp_defense", "sp_attack", "hp"]

    for stat in stats:
        stat_column = df.loc[:, stat].to_numpy()

        stat_to_quantiles["low " + stat] = (None, np.percentile(stat_column, 25))
        stat_to_quantiles["medium " + stat] = (np.percentile(stat_column, 25), np.percentile(stat_column, 75))
        stat_to_quantiles["high " + stat] = (np.percentile(stat_column, 75), None)

    return stat_to_quantiles


def generate_pokemon_to_stats_mapping(df: pd.DataFrame) -> Dict[Any, Dict[str, Any]]:
    """
    Generates a dictionary which maps a pokemon's name
    to a dictionary which maps stat names to their values.

    :param df:
        A pandas dataframe
    :return:
        A pokemon name to stats mapping
    """
    names = df.loc[:, "name"]
    attack = df.loc[:, "attack"]
    defense = df.loc[:, "defense"]
    sp_attack = df.loc[:, "sp_attack"]
    sp_defense = df.loc[:, "sp_defense"]
    speed = df.loc[:, "speed"]
    hp = df.loc[:, "hp"]
    pokedex_id = df.loc[:, "pokedex_number"]

    pokemon_to_stats = {}

    for i, name in enumerate(names):
        pokemon_to_stats[name] = {
            "attack": attack[i],
            "defense": defense[i],
            "sp_attack": sp_attack[i],
            "sp_defense": sp_defense[i],
            "speed": speed[i],
            "hp": hp[i],
            "pokedex_id": pokedex_id[i]
        }
    return pokemon_to_stats


def create_decision_tree(df: pd.DataFrame) -> DecisionTree:
    """
    Generates a decision tree using the pandas dataframe.
    The format, size, structure and purpose of this
    decision tree is all explicitly defined in the report with
    examples.

    :param df:
        Pandas dataframe
    :return:
        A decision Tree
    """

    # Create the base tree
    base_tree = DecisionTree(category=None, is_binary_parent=False, conversion_dictionary=None)
    stats = ["attack", "defense", "speed", "sp_defense", "sp_attack", "hp"]

    # Get all pokemon types
    types = np.unique(df.loc[:, "type1"].to_numpy())

    # Generate conversion dictionary
    conversion_dictionary = find_quantiles(df)
    pprint.pprint(conversion_dictionary)

    for pokemon_type in types:
        type_tree = DecisionTree(category=pokemon_type, is_binary_parent=False, conversion_dictionary=None)
        masked_df = mask_df(df, pokemon_type)

        for stat in stats:
            stat_tree = DecisionTree(category=stat, is_binary_parent=True,
                                     conversion_dictionary=conversion_dictionary)
            stat_tree.add_subtree(create_bst(masked_df.loc[:, "name"], masked_df.loc[:, stat]))
            type_tree.add_subtree(stat_tree)
        base_tree.add_subtree(type_tree)
    return base_tree


def mask_df(df: pd.DataFrame, pokemon_type: str) -> pd.DataFrame:
    """
    This function Takes a pokemon type and returns a pandas dataframe
    with only rows that contain pokemon of the given type

    :param df:
        A pandas dataframe
    :param pokemon_type:
        A pokemon type
    :return:
        A pandas dataframe with rows that only have
        pokemon of a given type. In other words, for every row,
        either the value in column type1 or the value in column type2 are
        equal to the passed in type
    """
    df_masked = df[(df["type1"] == pokemon_type) | (df["type2"] == pokemon_type)]
    return df_masked


def create_bst(names: np.ndarray, stat_list: np.ndarray) -> BinarySearchTree:
    """
    This function creates a BST given a numpy array of pokemon names
    and stat values.

    :param names:
        A numpy array of pokemon names
    :param stat_list:
        A list of a particular stat pokemon stat, where
        the pokemon at index i in names has a stat value
        equal to the value of stat_list at index i
    :return:
        A BST
    """
    names = names.to_numpy()
    stat_list = stat_list.to_numpy()

    new_bst = BinarySearchTree(None, None)

    for i, item in enumerate(stat_list):
        new_bst.insert(item, pokemon=names[i])

    return new_bst


def fetch_values(type_filter: str, stat: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes in a pokemon type, stat and pandas dataframe
    then returns a dataframe containing the specific stat values
    of all pokemon of the given type.

    :param type_filter:
        A pokemon type
    :param stat:
        A stat (ex: "attack")
    :param df:
        A pandas dataframe
    :return:
        A pandas dataframe which contains stat values
    """
    if type_filter == "all":
        return df.loc[:, stat]
    else:
        return mask_df(df, type_filter).loc[:, stat]
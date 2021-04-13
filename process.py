import pandas as pd
import numpy as np
from bst import BinarySearchTree
import pprint
from typing import List, Any, Optional
from decision_tree import DecisionTree


def read_data():
    df = pd.read_csv("data/pokemon.csv")
    return df


def find_quantiles(df) -> dict[str, float]:
    stat_to_quantiles = {}
    stats = ["attack", "defense", "speed", "sp_defense", "sp_attack", "hp"]

    for stat in stats:
        stat_column = df.loc[:, stat].to_numpy()

        stat_to_quantiles["low " + stat] = np.percentile(stat_column, 25)
        stat_to_quantiles["medium " + stat] = np.percentile(stat_column, 50)
        stat_to_quantiles["high " + stat] = np.percentile(stat_column, 75)

    return stat_to_quantiles


def generate_pokemon_to_stats_mapping(df):
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


def create_decision_tree(df):
    base_tree = DecisionTree(category=None, is_binary_parent=False)
    stats = ["attack", "defense", "speed", "sp_defense", "sp_attack", "hp"]

    types = np.unique(df.loc[:, "type1"].to_numpy())

    conversion_dictionary = find_quantiles(df)
    for pokemon_type in types:
        type_tree = DecisionTree(category=pokemon_type, is_binary_parent=False)
        masked_df = mask_df(df, pokemon_type)

        for stat in stats:
            stat_tree = DecisionTree(category=stat, is_binary_parent=True,
                                     conversion_dictionary=conversion_dictionary)
            stat_tree.add_subtree(create_bst(masked_df.loc[:, "name"], masked_df.loc[:, stat]))
            type_tree.add_subtree(stat_tree)
        base_tree.add_subtree(type_tree)
    return base_tree


def mask_df(df, pokemon_type):
    df_masked = df[(df["type1"] == pokemon_type) | (df["type2"] == pokemon_type)]
    return df_masked


def create_bst(names, stat_list) -> BinarySearchTree:
    names = names.to_numpy()
    stat_list = stat_list.to_numpy()

    new_bst = BinarySearchTree(None)

    for i, item in enumerate(stat_list):
        new_bst.insert(item, pokemon=names[i])

    return new_bst


def fetch_values(type_filter: str, stat: str, df):
    if type_filter == "all":
        return df.loc[:, stat]
    else:
        return mask_df(df, type_filter).loc[:, stat]

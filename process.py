import pandas as pd
import numpy as np
from bst import BinarySearchTree
import pprint
from typing import List, Any
from decision_tree import DecisionTree


# print(np.percentile(attack, 25))
# print(np.percentile(attack, 50))
# print(np.percentile(attack, 75))
# print("\n")
#
# print(np.percentile(defense, 25))
# print(np.percentile(defense, 50))
# print(np.percentile(defense, 75))
# print("\n")
#
# print(np.percentile(sp_attack, 25))
# print(np.percentile(sp_attack, 50))
# print(np.percentile(sp_attack, 75))
# print("\n")
#
# print(np.percentile(sp_defense, 25))
# print(np.percentile(sp_defense, 50))
# print(np.percentile(sp_defense, 75))
# print("\n")
#
# print(np.percentile(speed, 20))
# print(np.percentile(speed, 50))
# print(np.percentile(speed, 75))
#
# print("\n")
#
# print(np.percentile(hp, 25))
# print(np.percentile(hp, 50))
# print(np.percentile(hp, 75))
def read_data():
    df = pd.read_csv("data/pokemon.csv")
    return df


def find_quantiles(df) -> dict[str, dict[str, Any]]:
    stat_to_quantiles = {}
    stats = ["attack", "defense", "speed", "sp_defense", "sp_attack", "hp"]

    for stat in stats:
        stat_column = df.loc[:, stat].to_numpy()

        stat_to_quantiles["low " + stat] = np.percentile(stat_column, 25)
        stat_to_quantiles["medium " + stat] = np.percentile(stat_column, 25)
        stat_to_quantiles["high " + stat] = np.percentile(stat_column, 25)

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

    for pokemon_type in types:
        type_tree = DecisionTree(category=pokemon_type, is_binary_parent=False)
        masked_df = mask_df(df, pokemon_type)

        for stat in stats:
            stat_tree = DecisionTree(category=stat, is_binary_parent=True)
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

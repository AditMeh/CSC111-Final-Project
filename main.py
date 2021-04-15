"""
Program main
===============================
This is the main file of my project, which is responsible for all of the main computations.
Please read the instructions given below to see how to use this program.
===============================
This file is Copyright (c) 2021 Aditya Mehrotra.
"""
from gui import Gui
from process import read_data, create_decision_tree, generate_pokemon_to_stats_mapping


def main():
    df = read_data()
    decision_tree = create_decision_tree(df)
    pokemon_to_stats_mapping = generate_pokemon_to_stats_mapping(df)
    gui = Gui(df, decision_tree, pokemon_to_stats_mapping)
    gui.start_gui()


if __name__ == '__main__':
    main()

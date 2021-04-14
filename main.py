from gui import Gui
from process import read_data, create_decision_tree, generate_pokemon_to_stats_mapping


def main():
    df = read_data()
    decision_tree = create_decision_tree(df)
    pokemon_to_stats_mapping = generate_pokemon_to_stats_mapping(df)
    Gui(df, decision_tree, pokemon_to_stats_mapping)


if __name__ == '__main__':
    main()

"""
GUI Module
===============================
The functions/classes defined in this class are responsible for rendering
the pokemon recommendation GUI and processing user queries
===============================
This file is Copyright (c) 2021 Aditya Mehrotra.
"""

import PySimpleGUI as sg
from typing import List, Any, Dict
from process import fetch_values
from decision_tree import DecisionTree
import matplotlib.pyplot as plt

sg.theme('DarkAmber')


def check_query(q: str) -> bool:
    """
    This function check if a query is valid by making sure it is in the
    proper format. For more information about the format, please check
    the instructions to run my program in the project report.

    :param q:
        A query
    :return:
        A boolean which represents if the query is valid or not
    """
    # This won't cause an error since q is guaranteed to not equal an
    # empty string
    q = q.split(" ")

    # Establishing the sets which represent the valid types, stats and degrees
    type_set = {'flying', 'ice', 'psychic', 'ghost', 'water', 'ground', 'steel',
                'rock', 'fighting', 'fire', 'electric', 'poison', 'grass', 'bug', 'dark', 'normal', 'fairy',
                'dragon'}

    stat_set = {'attack', 'defense', 'sp_attack', 'sp_defense', 'hp', 'speed'}

    degree_set = {"high", "medium", "low"}

    if len(q) == 4:
        if q[0] in {'find', 'plot'} and q[1] in type_set and \
                q[2] in degree_set and q[3] in stat_set:
            return True
        else:
            return False
    else:
        return False


class Gui:
    """
    A class that contains all the methods and data that is required
    to run the pokemon recommender GUI.


    Private Instance Attributes:
        - df: pandas dataframe after loading in our data
        - decsion_tree: A decision tree used to process queries using the
        evaulate method
        - pokemon_to_stats: A dictionary that returns a pokemon's stats given
        their name
        - query: the query (after being converted to a list) give by the user
        - previous_search: Represents the last query made by the user, empty if
        no such query exists
        - party: a list of all pokemon in the party, an element in the
        list is "blank" if there is no pokemon at that posiiton

    Representation invariants:
        - len(self.party) == 6
    """

    def __init__(self, df, decision_tree: DecisionTree, pokemon_to_stats: Dict[Any, Dict[str, Any]]) -> None:
        """
        This function initializes the necessary datatypes for generating and
        rendering the BST with the query functions.

        :param df:
            pandas dataframe created after loading in the dataset
        :param decision_tree:
            A decision tree that is used to process user queries
        :param pokemon_to_stats:
            A mapping which converts pokemon into their stats
        """
        self.party = ["blank", "blank", "blank", "blank", "blank", "blank"]
        self.query = []
        self.previous_search = ""

        # Creating data-based variables
        self.df = df
        self.decision_tree = decision_tree
        self.pokemon_to_stats = pokemon_to_stats

    def start_gui(self) -> None:
        """
        This function starts the GUI's main event loop and also renders the GUI
        The loop only exits when the user closes the GUI.

        :return:
            None
        """

        # Create layout for the first time and render window
        layout = self.generate_layout()
        sg.theme('DarkAmber')
        window = sg.Window('Pokemon recommender', layout, size=(600, 600))

        while True:  # The Event Loop
            event, values = window.read()
            print(event, values)

            # Loop terminates when the user closes the window
            if event == sg.WIN_CLOSED:
                break

            # CASE: The user presses the "No action" button
            elif event != "submit" and values[event] == "No action":
                pass

            # CASE: the user submits a query
            elif event == "submit":
                query = values["-IN-"]

                # CASE: the query is invalid, then create popup
                if query == "" or not check_query(q=query):
                    sg.popup("Malformed query. Please follow the query structures as outlined in the report")

                # CASE: The query is valid and the query type is a plot query
                elif query.split(" ")[0] == "plot":
                    # Draw the graph
                    values = query.split(" ")
                    self.previous_search = query
                    self.draw_plot(values[2], values[1])

                # CASE: The query is valid and the query is a pokemon search
                elif query.split(" ")[0] == "find":
                    # Evaluate the decision tree for the recommended pokemon
                    self.previous_search = query
                    self.query = self.decision_tree.evaluate(self.process_query())
                    layout = self.generate_layout()

                    window_new = sg.Window('Pokemon recommender', layout, size=(600, 600), finalize=True)
                    window.close()
                    window = window_new  # Rerender window with new layout

            # CASE: User has clicked on an action on a searched pokemon
            elif event.split(" ")[0] == "pokemon:":
                name = " ".join(event.split(" ")[1:])  # Extract the name

                # CASE: The user wants the stats of the clicked pokemon
                if values[event] == "Display Stats":
                    print(values[event])

                    info_text = self.generate_info_text(name)

                    # Display the pokemon
                    sg.popup_non_blocking(info_text, grab_anywhere=True, image="generation-viii/icons/" +
                                                                               str(self.pokemon_to_stats[name][
                                                                                       "pokedex_id"]) +
                                                                               ".png")
                # CASE: the user wants to add the pokemon to their party
                elif values[event] == "Add to party":
                    if self.add_to_party(name):
                        layout = self.generate_layout()

                        window_new = sg.Window('Pokemon recommender', layout, size=(600, 600), finalize=True)
                        window.close()
                        window = window_new  # Rerender window

            # CASE: The user clicked an action on a party pokemon
            elif event.split(" ")[0] == "party:":
                name = " ".join(event.split(" ")[1:])  # Extract the name

                # CASE: The user wants to remove the pokemon from the party
                if values[event] == "Remove from party":
                    self.remove_from_party(name)

                    # Regenerate window
                    layout = self.generate_layout()
                    window_new = sg.Window('Pokemon recommender', layout, size=(600, 600), finalize=True)
                    window.close()
                    window = window_new

                # CASE: The user wants to display the stats of the pokemon
                elif values[event] == "Display stats":

                    info_text = self.generate_info_text(name)

                    sg.popup_non_blocking(info_text, grab_anywhere=True, image="generation-viii/icons/" +
                                                                               str(self.pokemon_to_stats[name][
                                                                                       "pokedex_id"]) +
                                                                               ".png")

        window.close()  # Exit when we're done

    def generate_layout(self) -> List[Any]:
        """
        Generates a layout, which will be used to re-render the GUI

        :return:
            A widget layout used to render the GUI
        """

        # CASE: The user has opened the GUI for the first time
        if len(self.previous_search) == 0:
            party = self.generate_party()

            layout = [[sg.Text('Party List:')],
                      party,
                      [sg.Text('Enter your query here:'), sg.Input(key='-IN-', default_text=self.previous_search),
                       sg.Button('Submit', key="submit")]]

        # CASE: The user has made a query before, generate searched pokemon
        elif len(self.previous_search) > 0:
            party = self.generate_party()
            pokemon_list = self.generate_grid()

            layout = [[sg.Text('Party List:')],
                      party,
                      [sg.Text('Enter your query here:'), sg.Input(key='-IN-', default_text=self.previous_search),
                       sg.Button('Submit', key="submit")],
                      [sg.Column(pokemon_list, scrollable=True, vertical_scroll_only=True, expand_y=True,
                                 expand_x=True, vertical_alignment="center")]]

        return layout

    def generate_grid(self) -> List[Any]:
        """
        Generate a grid of pokemon, with max 6 pokemon per row
        each row is represented as a nested list of ButtonMenu elements

        :return:
            A layout of ButtonMenu elements used to represent the pokemon
            that the query returns
        """
        grid = []
        max_row = 6

        temp_row = []
        for i in range(len(self.query)):
            filename = "generation-viii/icons/" + str(self.pokemon_to_stats[self.query[i]]["pokedex_id"]) \
                       + ".png "

            temp_row.append(sg.ButtonMenu(self.query[i], size=(10, 20), key="pokemon: " + self.query[i],
                                          menu_def=['BLANK', ["Display Stats", "Add to party"]],
                                          image_filename=filename,
                                          text_color="white"))

            # Reached the final pokemon or max row size
            if len(temp_row) == max_row or i == len(self.query) - 1:
                grid.append(temp_row)
                temp_row = []
        return grid

    def generate_party(self) -> List[Any]:
        """
        Generate the row of party pokemon using the stored
        self.party variable

        :return:
            A list of ButtonMenu elemnts, representing the party of pokemon
        """
        party_grid = []
        for i in range(len(self.party)):
            if self.party[i] != "blank":
                filename = "generation-viii/icons/" + str(self.pokemon_to_stats[self.party[i]]["pokedex_id"]) \
                           + ".png "

                party_grid.append(sg.ButtonMenu(self.party[i], size=(10, 5), key="party: " + self.party[i],
                                                menu_def=['BLANK', ["Display stats", "Remove from party"]],
                                                image_filename=filename,
                                                auto_size_button=True))
            elif self.party[i] == "blank":
                party_grid.append(sg.ButtonMenu(self.party[i], size=(10, 5),
                                                menu_def=['BLANK', ["No action"]]))

        return party_grid

    def add_to_party(self, pokemon: str) -> bool:
        """
        Adds a pokemon to the user's party

        :param pokemon:
            A string, which corresponds to the name of the pokemon
            being added to the party
        :return:
            A boolean which represents whether the pokemon was added to the party
            or not
        """
        # CASE: Desired pokemon is already in your party, raise popup
        if pokemon in self.party:
            sg.popup(str(pokemon) + " is already in your party")
            return False  # A pokemon was not added to the party

        # CASE:  The party is full
        elif all(item != "blank" for item in self.party):
            sg.popup("Party size is already at the max, please remove a pokemon to add a new one")
            return False  # A pokemon was not added to the party

        # CASE: The pokemon can be added to the party
        else:
            for i in range(len(self.party)):
                if self.party[i] == "blank":
                    self.party[i] = pokemon
                    return True  # A pokemon was added to the party

    def generate_info_text(self, name: str) -> str:
        """
        This function generates a string that will be rendered on the
        "Display stats" popup for a given pokemon. The string
        contains the stats and name of the pokemon

        :param name:
            The name of the pokemon that the info string
            will be made for
        :return:
            Returns the text that will be rendered in the
            "Display stats" popup
        """
        info_text = name + ":" + "\n" + "\n" + "Attack: " + str(
            self.pokemon_to_stats[name]["attack"]) + "\n" + "\n" + "Speed: " + str(
            self.pokemon_to_stats[name]["speed"]) + "\n" + "\n" + "HP: " + str(
            self.pokemon_to_stats[name]["hp"]) + "\n" + "\n" + "Special Attack: " + str(
            self.pokemon_to_stats[name]["sp_attack"]) + "\n" + "\n" + "Special Defense: " + str(
            self.pokemon_to_stats[name]["sp_defense"])
        return info_text

    def remove_from_party(self, pokemon: str) -> None:
        """
        Removes a pokemon from the party

        :param pokemon:
            The pokemon to be removed
        :return:
            Nothing
        """
        # Iterate through the party, searching for a the pokemon
        for i in range(len(self.party)):
            if self.party[i] == pokemon:
                # Replace the pokemon with "blank", since the spot is now empty

                self.party[i] = "blank"
                break

    def process_query(self) -> List[str]:
        """
        Converts a query into the format required for the
        DecisionTree to evaluate the query

        :return:
            A List which is formatted in the following form:
            ["type", "stat", "degree" + " " + "stat"]
        """
        typing, degree, stat = self.previous_search.split()[1:]
        conversion_key = degree + " " + stat
        return [typing, stat, conversion_key]

    def draw_plot(self, stat: str, typing: str) -> None:
        """
        This function draws a matplotlib histogram of the stat values
        of all pokemon of a certain typing

        :param stat:
            Desired stat used to fetch data to create the histogram
        :param typing:
            Pokemon typing that will be used to extract a subset
            of all pokemon
        :return:
            None
        """
        # Close any open plots
        plt.clf()
        plt.cla()
        plt.close()

        # Generate the figure
        plt.figure(num='Query: ' + self.previous_search)
        lst = fetch_values(typing, stat, self.df)
        plt.hist(lst, density=False, bins=50)
        plt.title("A histogram of the " + stat + " of " + typing + " pokemon")
        plt.xlabel(stat + " values")
        plt.ylabel("Count")

        plt.show(block=False)

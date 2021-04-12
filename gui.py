import PySimpleGUI as sg
from typing import List
from process import read_data, create_decision_tree, generate_pokemon_to_stats_mapping, fetch_values
import matplotlib.pyplot as plt

sg.theme('DarkAmber')


class Gui:
    def __init__(self):
        self.party = ["blank", "blank", "blank", "blank", "blank", "blank"]
        self.query = []
        self.previous_search = ""

        # Creating data-based variables
        self.df = read_data()
        self.decision_tree = create_decision_tree(self.df)
        self.pokemon_to_stats = generate_pokemon_to_stats_mapping(self.df)

        layout = self.generate_layout()
        sg.theme('DarkAmber')
        window = sg.Window('Pokemon recommender', layout, size=(600, 600))

        while True:  # The Event Loop
            event, values = window.read()
            print(event, values)
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            elif event == "submit":
                query = values["-IN-"]
                if query == "":
                    pass
                elif query.split(" ")[0] == "plot":
                    values = query.split(" ")
                    self.draw_plot(values[2], values[1])

                else:
                    self.previous_search = query
                    self.query = self.decision_tree.evaluate(self.process_query())
                    layout = self.generate_layout()

                    window_new = sg.Window('Pokemon recommender', layout, size=(600, 600), finalize=True)
                    window.close()
                    window = window_new

            elif event.split(" ")[0] == "pokemon:":
                name = " ".join(event.split(" ")[1:])

                if values[event] == "Display Stats":
                    print(values[event])

                    info_text = self.generate_info_text(name)

                    sg.popup_non_blocking(info_text, grab_anywhere=True, image="generation-viii/icons/" +
                                                                               str(self.pokemon_to_stats[name][
                                                                                       "pokedex_id"]) +
                                                                               ".png")
                elif values[event] == "Add to party":
                    if self.add_to_party(name):
                        layout = self.generate_layout()

                        window_new = sg.Window('Pokemon recommender', layout, size=(600, 600), finalize=True)
                        window.close()
                        window = window_new

            elif event.split(" ")[0] == "party:":
                name = " ".join(event.split(" ")[1:])

                if values[event] == "Remove from party":
                    self.remove_from_party(name)

                    # Regenerate window
                    layout = self.generate_layout()
                    window_new = sg.Window('Pokemon recommender', layout, size=(600, 600), finalize=True)
                    window.close()
                    window = window_new

                elif values[event] == "Display stats":
                    print(values[event])

                    info_text = self.generate_info_text(name)

                    sg.popup_non_blocking(info_text, grab_anywhere=True, image="generation-viii/icons/" +
                                                                               str(self.pokemon_to_stats[name][
                                                                                       "pokedex_id"]) +
                                                                               ".png")

        window.close()

    def generate_layout(self) -> List:

        # Default case:
        if len(self.previous_search) == 0:
            party = self.generate_party()
            # pokemon_list = self.generate_grid(query_result)

            layout = [[sg.Text('Party List:')],
                      party,
                      [sg.Text('Enter your query here:'), sg.Input(key='-IN-', default_text=self.previous_search),
                       sg.Button('Submit', key="submit")]]

        # Case if a query was made
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

    def generate_grid(self) -> List:
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
            if len(temp_row) == max_row or i == len(self.query) - 1:
                grid.append(temp_row)
                temp_row = []
        return grid

    def generate_party(self) -> List:
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
        if pokemon in self.party:
            sg.popup(str(pokemon) + " is already in your party")
            return False
        elif all(item != "blank" for item in self.party):
            sg.popup("Party size is already at the max, please remove a pokemon to add a new one")
            return False
        else:
            for i in range(len(self.party)):
                if self.party[i] == "blank":
                    self.party[i] = pokemon
                    return True

    def generate_info_text(self, name):
        info_text = name + ":" + "\n" + "\n" + "Attack: " + str(
            self.pokemon_to_stats[name]["attack"]) + "\n" + "\n" + "Speed: " + str(
            self.pokemon_to_stats[name]["speed"]) + "\n" + "\n" + "HP: " + str(
            self.pokemon_to_stats[name]["hp"]) + "\n" + "\n" + "Special Attack: " + str(
            self.pokemon_to_stats[name]["sp_attack"]) + "\n" + "\n" + "Special Defense: " + str(
            self.pokemon_to_stats[name]["sp_defense"])
        return info_text

    def remove_from_party(self, pokemon: str) -> None:
        for i in range(len(self.party)):
            if self.party[i] == pokemon:
                self.party[i] = "blank"
                break

    def process_query(self):
        # perhaps more preprocessing code here
        type, stat, threshold = self.previous_search.split()
        threshold = int(threshold)
        return [type, stat, threshold]

    def draw_plot(self, stat, typing):
        plt.clf()
        plt.cla()
        plt.close()

        lst = fetch_values(typing, stat, self.df)
        plt.hist(lst, density=True, bins=30)
        plt.show(block=False)



Gui()

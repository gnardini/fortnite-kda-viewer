import numpy as np
import time
import tkinter as tk

class OutputScreen:
    def __init__(self, enabled=True):
        root = tk.Tk()
        root.title('KDA Viewer')
        root.geometry("500x500")
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        tk.Label(root, text='Kills', font='Helvetica 18 bold', padx=10, pady=10).grid(row=0, column=0, sticky=tk.W)
        tk.Label(root, text='Killer', font='Helvetica 18 bold', padx=10, pady=10).grid(row=2, column=0, sticky=tk.W)
        tk.Label(root, text='Leaderboard', font='Helvetica 18 bold', padx=10, pady=10).grid(row=0, column=1, sticky=tk.W)

        self.kills = tk.StringVar()
        self.killer = tk.StringVar()
        self.leaderboard = tk.StringVar()

        tk.Message(root, textvariable=self.kills, width=230, padx=10).grid(row=1, column=0, sticky=tk.W)
        tk.Message(root, textvariable=self.killer, width=230, padx=10).grid(row=3, column=0, sticky=tk.W)
        tk.Message(root, textvariable=self.leaderboard, width=230, padx=10).grid(row=1, column=1, rowspan=3, sticky=tk.W+tk.N)

        self.root = root

        if enabled:
            self.root.update()

    # players_info looks like this:
    # {
    #   'player_kills': [('nardiii', 'Streamer[342]')],
    #   'player_deaths': [],
    #   'other_kills': [('SaindoComSuaMae', 'Koringa._Da_Rpg'),
    #                   ('', 'Streamer[342]'),
    #                   ('FC99', 'TheKillerNight54'),
    #                   ('Gsb1612', 'Wolfraind'),
    #                   ('SaindoComSuaMae', 'Koringa._Da_Rpg')]
    # }
    def update_players_info(self, players_info):
        killed_names = [pair[1].strip() for pair in players_info['other_kills']]
        killer_names = [pair[1].strip() for pair in players_info['player_deaths']]
        self.kills.set('\n'.join(killed_names))
        self.killer.set('\n'.join(killer_names))
        self.leaderboard.set('TODO') # TODO
        self.root.update()

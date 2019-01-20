import numpy as np
import time
import tkinter as tk

class OutputScreen:
    def __init__(self, enabled=True):
        self.enabled = enabled
        root = tk.Tk()
        root.title('KDA Viewer')
        root.geometry("500x500")
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        tk.Label(root, text='Kills', font='Helvetica 18 bold', padx=10, pady=10).grid(row=0, column=0, sticky=tk.W+tk.S)
        tk.Label(root, text='Killer', font='Helvetica 18 bold', padx=10, pady=10).grid(row=2, column=0, sticky=tk.W+tk.S)
        tk.Label(root, text='Leaderboard', font='Helvetica 18 bold', padx=10, pady=10).grid(row=0, column=1, sticky=tk.W+tk.S)

        self.kills = tk.StringVar()
        self.killer = tk.StringVar()
        self.leaderboard = tk.StringVar()

        self.killed_names = []
        self.killer_names = []
        self.all_kills = {}
        self.player_name = None

        tk.Message(root, textvariable=self.kills, width=230, padx=10).grid(row=1, column=0, sticky=tk.W+tk.N)
        tk.Message(root, textvariable=self.killer, width=230, padx=10).grid(row=3, column=0, sticky=tk.W+tk.N)
        tk.Message(root, textvariable=self.leaderboard, width=230, padx=10).grid(row=1, column=1, rowspan=3, sticky=tk.W+tk.N)

        self.root = root

        if enabled:
            self.root.update()

    # players_info looks like this:
    # {
    #   'player_kills': [('nardiii', 'Streamer[342]', 'rifle')],
    #   'player_deaths': [],
    #   'other_kills': [('SaindoComSuaMae', 'Koringa._Da_Rpg', 'shotgun'),
    #                   ('', 'Streamer[342]', None),
    #                   ('FC99', 'TheKillerNight54', 'splodes'),
    #                   ('Gsb1612', 'Wolfraind', 'rifle'),
    #                   ('SaindoComSuaMae', 'Koringa._Da_Rpg', 'rifle')]
    # }
    def update_players_info(self, players_info):
        killed_names = [pair[1].strip() for pair in players_info['player_kills']]
        killer_names = [pair[0].strip() for pair in players_info['player_deaths']]

        for killed in killed_names:
            if killed not in self.killed_names and self.is_name(killed):
                self.killed_names.append(killed)
                self.player_name = players_info['player_kills'][0][0]
        for killer in killer_names:
            if killer not in self.killer_names and self.is_name(killer):
                self.killer_names.append(killer)

        for kill in players_info['other_kills']:
            if self.is_name(kill[0]):
                if kill[0] not in self.all_kills:
                    self.all_kills[kill[0]] = []
                self.all_kills[kill[0]].append(kill[1])


        all_kills = { k: len(v) for k, v in self.all_kills.items() }
        if self.player_name != None:
            all_kills[self.player_name] = len(self.killed_names)
        ordered_kills = sorted(all_kills.items(), key=lambda x: -x[1])
        all_kills_text = [x[0] + ': ' + str(x[1]) for x in ordered_kills]

        print('Total: %d' % sum([x[1] for x in all_kills.items()]))

        self.kills.set('\n'.join(self.killed_names))
        self.killer.set('\n'.join(self.killer_names))
        self.leaderboard.set('\n'.join(all_kills_text))

        if self.enabled:
            self.root.update()

    def is_name(self, text):
        return text.replace(' ', '').replace('.', '').replace('_', '').replace('?', '') != ""

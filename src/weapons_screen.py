import numpy as np
import time
import tkinter as tk

class WeaponsScreen:
    def __init__(self, enabled=True):
        self.enabled = enabled
        root = tk.Tk()
        root.title('FN Corner')
        root.geometry("500x500")
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        tk.Label(root, text='Own', font='Helvetica 18 bold', padx=10, pady=10).grid(row=0, column=0, sticky=tk.W+tk.S)
        tk.Label(root, text='Total', font='Helvetica 18 bold', padx=10, pady=10).grid(row=0, column=1, sticky=tk.W+tk.S)

        self.own = tk.StringVar()
        self.total = tk.StringVar()

        self.player_kills = []
        self.saved_kills = []

        tk.Message(root, textvariable=self.own, width=230, padx=10).grid(row=1, column=0, sticky=tk.W+tk.N)
        tk.Message(root, textvariable=self.total, width=230, padx=10).grid(row=1, column=1, rowspan=3, sticky=tk.W+tk.N)

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
        self.add_kills(players_info['player_kills'], lambda kill: self.player_kills.append(kill))
        self.add_kills(players_info['player_deaths'])
        self.add_kills(players_info['other_kills'])

        player_kill_weapons = [kill[2] for kill in self.player_kills]
        all_kills_weapons = [kill[2] for kill in self.saved_kills]

        player_weapons_count = {}
        all_weapons_count = {}

        for weapon in player_kill_weapons:
            if weapon not in player_weapons_count:
                player_weapons_count[weapon] = 0
            player_weapons_count[weapon] += 1

        for weapon in all_kills_weapons:
            if weapon not in all_weapons_count:
                all_weapons_count[weapon] = 0
            all_weapons_count[weapon] += 1

        self.own.set('\n'.join(['%s: %d' % (weapon, count) for weapon, count in player_weapons_count.items()]))
        self.total.set('\n'.join(['%s: %d' % (weapon, count) for weapon, count in all_weapons_count.items()]))

        if self.enabled:
            self.root.update()

    def add_kills(self, kills_info, save_kill_fn = lambda x: None):
        for (killer, killed, weapon) in kills_info:
            killer = killer.strip()
            killed = killed.strip()
            kill = (killer, killed, weapon)
            if self.is_name(killer) and self.is_name(killed) and kill not in self.saved_kills:
                if weapon == None:
                    print(kill)
                self.saved_kills.append(kill)
                save_kill_fn(kill)

    def is_name(self, text):
        return text.replace(' ', '').replace('.', '').replace('_', '').replace('?', '') != ""

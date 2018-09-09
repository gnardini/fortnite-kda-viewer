import numpy as np
import requests
import json
import configparser

class FortniteApi:

    def __init__(self, config):
        self.base_url = 'https://api.fortnitetracker.com/v1/profile/pc/'
        self.headers = {
            'TRN-Api-Key': config['DEFAULT']['TRN_KEY']
        }

    # TODO: Read the response header to see if we need to wait due to the API rate limiting.
    def find_player_kda(self, player):
         r = requests.get(self.base_url + player, headers = self.headers)
         data = r.json()
         solo = data['stats']['curr_p2']
         duo = data['stats']['curr_p10']
         squad = data['stats']['curr_p9']
         matches = 0
         wins = 0
         kills = 0
         for stats in [solo, duo, squad]:
             matches = matches + stats['matches']['valueInt']
             kills = kills + stats['kills']['valueInt']
             wins = wins + stats['top1']['valueInt']
         return {
            'kd': "%.2f" % (kills / (matches - wins)),
            'win_percent': "%.2f" % (100 * wins / matches)
         }

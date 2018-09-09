import game_screen as gs
import vision as v
import fortnite_api as fa
import output_screen as os
import time
import configparser

def log(self, text):
    print('[%s] %s' % (time.strftime('%H:%M:%S'), text))

config = configparser.ConfigParser()
config.read('config.ini')
vision = v.Vision()
gamescreen = gs.GameScreen(vision)
api = fa.FortniteApi(config)
screen = os.OutputScreen(vision)

kdas = {}

while(True):
    vision.refresh_frame()
    players = gamescreen.find_players()
    for playerIndex in players: # TODO check this (access item directly).
        player = players[playerIndex]
        if kdas[player] == None: # Check if correct
            kda = api.find_player_kda(player)
            print("%s: %d"  % (player, kda))
            kdas[player] = {
                'kda': kda,
                'timestamp': time.perf_counter()
            }
    min_timstamp = time.perf_counter() - 5
    players_to_show = filter(kdas, lambda x: x.timestamp >= min_timstamp)
    screen.show_players(players_to_show)
    # Sleep only 5 seconds while in game but more time when not in game.
    time.sleep(5)

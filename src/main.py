import game_screen as gs
import vision as v
import fortnite_api as fa
import output_screen as os
import letters_classifier as lc
import time
import configparser

def log(text):
    print('[%s] %s' % (time.strftime('%H:%M:%S'), text))

config = configparser.ConfigParser()
config.read('config.ini')
vision = v.Vision()
classifier = lc.LettersClassifier()
gamescreen = gs.GameScreen(vision, classifier)
api = fa.FortniteApi(config)
screen = os.OutputScreen()

kdas = {}

while(True):
    start_all = time.perf_counter()
    start = start_all

    vision.refresh_frame()

    print('take screenshot: %f' % (time.perf_counter() - start))
    start = time.perf_counter()

    # players = gamescreen.find_players()
    vision.save_frame()

    print('save frame: %f' % (time.perf_counter() - start))
    start = time.perf_counter()



    # for playerIndex in players: # TODO check this (access item directly).
    #     player = players[playerIndex]
    #     if kdas[player] == None: # Check if correct
    #         kda = api.find_player_kda(player)
    #         print("%s: %d"  % (player, kda))
    #         kdas[player] = {
    #             'kda': kda,
    #             'timestamp': time.perf_counter()
    #         }
    # min_timstamp = time.perf_counter() - 5
    # players_to_show = filter(kdas, lambda x: x.timestamp >= min_timstamp)
    # screen.show_players(players_to_show)
    # Sleep only 5 seconds while in game but more time when not in game.
    time.sleep(5)
    print('sleep: %f' % (time.perf_counter() - start))
    print('ALL: %f' % (time.perf_counter() - start_all))

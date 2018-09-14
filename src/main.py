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
screen = os.OutputScreen(True)

kdas = {}

frame_number = 14
max_frame = 266
vision.frame_number = frame_number

while(True):
    start = time.perf_counter()

    # vision.refresh_frame()
    vision.read_frame()

    players = gamescreen.find_players()
    screen.update_players_info(players)

    frame_number = frame_number + 1
    if frame_number == max_frame:
        while(True):
            time.sleep(1)



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

    print('Time: %f' % (time.perf_counter() - start))
    if frame_number%10 == 0:
        time.sleep(1)

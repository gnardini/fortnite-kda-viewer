from src import game_screen as gs
from src import vision as v
from src import letters_classifier as lc
from src import output_screen as os
from pprint import pprint

vision = v.Vision()
classifier = lc.LettersClassifier()
gamescreen = gs.GameScreen(vision, classifier)
screen = os.OutputScreen(False)

vision.frame_number = 1
max_frame = 266

while(vision.frame_number < max_frame):
    vision.read_frame()

    players = gamescreen.find_players()
    screen.update_players_info(players)

pprint(screen.all_kills)

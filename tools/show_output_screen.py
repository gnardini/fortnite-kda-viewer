import os
import time
import cv2
from src import output_screen
from src import game_screen as gs
from src import letters_classifier as lc
from src import vision as v

vision = v.Vision()
classifier = lc.LettersClassifier()
gamescreen = gs.GameScreen(vision, classifier)
screen = output_screen.OutputScreen()

def read_image(path):
    file_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'test', 'screenshots', path)
    img = cv2.imread(file_path)
    vision.frame = img[800:950, :460, :]

read_image('screenshot116.png')
players_info = gamescreen.find_players()

while True:
    screen.update_players_info(players_info)
    # time.sleep(5)

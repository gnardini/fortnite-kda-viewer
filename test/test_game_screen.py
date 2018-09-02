from src import game_screen as gs
from src import vision as v
from src import letters_classifier as c
import os
import cv2
import unittest

class GameScreenTests(unittest.TestCase):
    def setUp(self):
        self.vision = v.Vision()
        self.classifier = c.LettersClassifier()
        self.game_screen = gs.GameScreen(self.vision, self.classifier)

    def test_find_players(self):
        print()
        i = 1
        while i <= 39:
            file = 'screenshot' + str(i)
            self.read_image('screenshots/%s.png' % file)
            players = self.game_screen.find_players(print_mask=False, save_letters=True, file_name='white/' + file)
            i = i+1
            print(players)

    def read_image(self, path):
        file_path = os.path.join(os.path.split(__file__)[0], path)
        img = cv2.imread(file_path)
        self.vision.frame = img

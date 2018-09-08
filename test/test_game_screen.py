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
        # 37, 39, 40, 50, 55
        # last = 97
        min = 135
        max = 135
        i = min
        while i <= max:
            file = 'screenshot' + str(i)
            self.read_image('screenshots/%s.png' % file)
            players_info = self.game_screen.find_players(print_mask=False, save_letters=False, file_name='white/' + file)
            print('-----')
            print('File %s' % file)
            all_kills = players_info['player_kills'] + players_info['player_deaths'] + players_info['other_kills']
            for kill in all_kills:
                print('%s killed: %s' % kill)
            i = i+1

    def read_image(self, path):
        file_path = os.path.join(os.path.split(__file__)[0], path)
        img = cv2.imread(file_path)
        print(file_path)
        self.vision.frame = img

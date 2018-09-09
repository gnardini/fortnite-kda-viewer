from src import game_screen as gs
from src import vision as v
from src import letters_classifier as c
import os
import cv2
import unittest
import time

class GameScreenTests(unittest.TestCase):
    def setUp(self):
        self.vision = v.Vision()
        self.classifier = c.LettersClassifier()
        self.game_screen = gs.GameScreen(self.vision, self.classifier)

    def test_find_players(self):
        print()
        min = 1
        max = 1
        i = min
        times = 0
        while i <= max:
            file = 'screenshot' + str(i)
            self.read_image('%s.png' % file)

            start = time.perf_counter()
            players_info = self.game_screen.find_players(print_mask=False, save_letters=False, file_name='white/' + file)
            time_diff = time.perf_counter() - start
            times = times + time_diff
            print('-----')
            print('File %s took %f' % (file, time_diff))

            # all_kills = players_info['player_kills'] + players_info['player_deaths'] + players_info['other_kills']
            # for kill in all_kills:
                # print('%s killed: %s' % kill)
            i = i+1
        print('Average: %f' % (times / max))

    def test_player_from_text(self):
        self.assertEqual('pepito', self.game_screen.player_from_white_text('pepito shotgunned someone else'))
        self.assertEqual('pepito capo', self.game_screen.player_from_white_text('pepito capo sploded someone else'))
        self.assertEqual('pepito', self.game_screen.player_from_white_text('pepito eljmlnated someone else'))
        self.assertEqual('pepito', self.game_screen.player_from_white_text('pepito bludgoneddd someone else'))
        self.assertEqual('pepito', self.game_screen.player_from_white_text('pepito nearly claared out someone else'))
        self.assertEqual('pepito', self.game_screen.player_from_white_text('pepito finallyeliminated'))
        self.assertEqual('pepito', self.game_screen.player_from_white_text('pepito shotgunned'))
        self.assertEqual('pepito', self.game_screen.player_from_white_text('pepito nearly .sploded (60 m)'))

    def read_image(self, path):
        file_path = os.path.join(os.path.split(__file__)[0], 'screenshots', path)
        img = cv2.imread(file_path)
        self.vision.frame = img[800:950, :460, :]

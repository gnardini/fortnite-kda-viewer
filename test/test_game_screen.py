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

    # 118 benchmark:
    # Original: 1.331464
    # Common letters first: 0.645694
    def test_find_players(self):
        print()
        min = 118
        max = 118
        i = min
        while i <= max:
            file = 'screenshot' + str(i)
            self.read_image('%s.png' % file)
            players_info = self.game_screen.find_players(print_mask=False, save_letters=False, file_name='white/' + file)
            print('-----')
            print('File %s' % file)
            all_kills = players_info['player_kills'] + players_info['player_deaths'] + players_info['other_kills']
            for kill in all_kills:
                print('%s killed: %s' % kill)
            i = i+1

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

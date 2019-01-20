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
        min = 81
        max = 81
        i = min
        times = 0
        while i <= max:
            # file = 'screenshot' + str(i)
            file = 'frame-' + str(i)
            self.read_image('%s.png' % file)

            start = time.perf_counter()
            players_info = self.game_screen.find_players(print_mask=True, save_letters=False, file_name='white/' + file)
            time_diff = time.perf_counter() - start
            times = times + time_diff
            print('-----')
            print('File %s took %f' % (file, time_diff))

            all_kills = players_info['player_kills'] + players_info['player_deaths'] + players_info['other_kills']
            for kill in all_kills:
                print('%s killed %s with a %s' % kill)
            i = i+1
        print('Average: %f' % (times / max))

    def test_player_from_text(self):
        self.assert_kill_with_weapon('pepito', 'shotgun', 'pepito shotgunned someone else')
        self.assert_kill_with_weapon('pepito capo', 'splodes', 'pepito capo sploded someone else')
        self.assert_kill_with_weapon('pepito', 'rifle', 'pepito eljmlnated someone else with a rifle')
        self.assert_kill_with_weapon('pepito', 'pickaxe', 'pepito bludgoneddd someone else')
        self.assert_kill_with_weapon('pepito', 'clear', 'pepito nearly claared out someone else')
        self.assert_kill_with_weapon('pepito', None, 'pepito finallyeliminated')
        self.assert_kill_with_weapon('pepito', 'shotgun', 'pepito shotgunned')
        self.assert_kill_with_weapon('pepito', 'splodes', 'pepito nearly .sploded (60 m)')

    def assert_kill_with_weapon(self, killer, weapon, phrase):
        info = self.game_screen.info_from_white_text(phrase)
        self.assertEqual(killer, info['killer'])
        self.assertEqual(weapon, info['weapon'])

    def read_image(self, path):
        # file_path = os.path.join(os.path.split(__file__)[0], 'screenshots', path)
        # img = cv2.imread(file_path)
        # self.vision.frame = img[800:950, :460, :]

        file_path = os.path.join(os.path.split(os.path.split(__file__)[0])[0], 'out', 'full_game', path)
        self.vision.frame = cv2.imread(file_path)

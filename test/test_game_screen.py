from src import game_screen as gs
from src import vision as v
import cv2
import unittest

class GameScreenTests(unittest.TestCase):
    def setUp(self):
        self.vision = v.Vision()
        self.game_screen = gs.GameScreen(self.vision)

    def test_find_players(self):
        file = 'screenshot3'
        self.read_image('screenshots/%s.png' % file)
        players = self.game_screen.find_players(True, file)
        print(players)

    def read_image(self, path):
        file_path = '/'.join(__file__.split('/')[:-1]) + '/' + path
        img = cv2.imread(file_path)
        self.vision.frame = img

from src import game_screen as gs
from src import vision as v
import cv2
import unittest



class GameScreenTests(unittest.TestCase):
    def setUp(self):
        self.vision = v.Vision()
        self.game_screen = gs.GameScreen(self.vision)

    def test_find_players(self):
        self.read_image('screenshots/screenshot.png')
        players = self.game_screen.find_players()
        print(players)

    def read_image(self, path):
        file_path = '/'.join(__file__.split('/')[:-1]) + '/' + path
        img = cv2.imread(file_path)
        self.vision.frame = img

if __name__ == '__main__':
    unittest.main()

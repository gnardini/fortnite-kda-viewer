from src import vision as v
import unittest
import cv2

class VisionTests(unittest.TestCase):
    def setUp(self):
        self.vision = v.Vision()

    # def test_take_screenshot(self):
    #     self.vision.refresh_frame()
    #     cv2.imshow('image', self.vision.frame)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

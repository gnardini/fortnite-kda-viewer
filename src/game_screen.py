import numpy as np
import time
import cv2
import pytesseract

class GameScreen:
    def __init__(self, vision):
        self.vision = vision

        self.names_color_min = [170, 40, 45]
        self.names_color_max = [250, 120, 150]
        self.player_name_color_min = [60, 140, 70]
        self.player_name_color_max = [120, 200, 120]

        self.names_color_min.reverse()
        self.names_color_max.reverse()
        self.player_name_color_min.reverse()
        self.player_name_color_max.reverse()

    def find_players(self):
        screen = self.vision.frame
        shape = screen.shape

        height = shape[0]//4
        rect = screen[(shape[0]-height*3//2):shape[0]-height//2, 0:shape[1]//4]

        other_names_mask = self.apply_mask(rect, self.names_color_min, self.names_color_max)
        player_name_mask = self.apply_mask(rect, self.player_name_color_min, self.player_name_color_max)

        player_name_mask = cv2.erode(player_name_mask, np.ones((1, 1),np.uint8))
        player_name_mask = cv2.dilate(player_name_mask, np.ones((1, 1),np.uint8))

        other_names_mask = cv2.dilate(other_names_mask, np.ones((1, 1),np.uint8))
        # other_names_mask = cv2.erode(other_names_mask, np.ones((1, 1),np.uint8))
        # other_names_mask = cv2.dilate(other_names_mask, np.ones((1, 1),np.uint8))

        print(pytesseract.image_to_data(other_names_mask))
        print(pytesseract.image_to_data(player_name_mask))

        cv2.imshow('image', player_name_mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Run OCR over other_names_mask and player_name_mask.
        # Check for first and last word in lines and keep only the ones where
        # values are at the same y value.

    def apply_mask(self, img, min, max):
         mask = cv2.inRange(img, np.array(min, dtype=np.uint8),
               np.array(max, dtype=np.uint8))
         return cv2.bitwise_and(img, img, mask = mask)

    # Not implemented yet, future optimization
    def find_names_color(self):
        screen = self.vision.frame
        # Get a small square on the bottom left, compare with names_color, assign
        # the color that is the closest.
        # Or use OCR to find the place of the words and then check the color there.

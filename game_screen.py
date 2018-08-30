import numpy as np
import time

class GameScreen:
    names_color = [0, 0, 0]
    player_name_color = [0, 0, 0]

    def __init__(self, vision):
        self.vision = vision

    def find_players(self):
        screen = vision.frame
        # Use two masks with the color |names_color| and |player_name_collor|
        # and apply them. Run OCR over places with values.
        # Check for first and last word in lines and keep only the ones where
        # values are at the same y value.


        # np.shape(matches)[1] >= 1


    # Not implemented yet, future optimization
    def find_names_color(self):
        screen = vision.frame
        # Get a small square on the bottom left, compare with names_color, assign
        # the color that is the closest.
        # Or use OCR to find the place of the words and then check the color there.

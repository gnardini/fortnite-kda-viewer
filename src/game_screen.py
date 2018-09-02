import numpy as np
import time
import cv2
from PIL import Image
import os
import random

class GameScreen:
    def __init__(self, vision):
        self.vision = vision

        self.names_color_min = [0, 50, 50]
        self.names_color_max = [10, 250, 255]
        self.player_name_color_min = [0, 50, 50]
        self.player_name_color_max = [20, 255, 255]

        # self.names_color_min.reverse()
        # self.names_color_max.reverse()
        # self.player_name_color_min.reverse()
        # self.player_name_color_max.reverse()

    def find_players(self, save_letters=False, file_name=None):
        screen = self.vision.frame
        # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
        shape = screen.shape

        height = shape[0]//4
        rect = screen[(shape[0]-height*3//2):shape[0]-height//2, 0:shape[1]//4]

        other_names_mask = self.apply_mask(rect, self.names_color_min, self.names_color_max)
        player_name_mask = self.apply_mask(rect, self.player_name_color_min, self.player_name_color_max)

        other_players = self.find_name_imgs(other_names_mask)
        last_index = 1
        for other in other_players:
            letters = self.separate_letters(other)
            if save_letters:
                for letter in letters:
                    letter = self.crop_image(letter)
                    path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/dataset/' + file_name + '-' + str(last_index) + '.png'
                    cv2.imwrite(path, letter)
                    last_index = last_index + 1

        # TODO: If not save_letters do something with this.
        player = self.find_name_imgs(player_name_mask)


        cv2.imshow('image', other_names_mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def apply_mask(self, img, min, max):
         mask = cv2.inRange(img, np.array([60, 80, 160], dtype=np.uint8),
               np.array([110, 100, 220], dtype=np.uint8))
         mask = cv2.bitwise_and(img, img, mask = mask)
         mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)

         # mask2 = cv2.inRange(img, np.array([160, 50, 50], dtype=np.uint8),
         #      np.array([179, 255, 255], dtype=np.uint8))
         # mask2 = cv2.bitwise_and(img, img, mask = mask2)
         # mask2 = cv2.cvtColor(mask2,cv2.COLOR_BGR2GRAY)
         #
         # mask = cv2.bitwise_or(mask, mask2)

         ignore,mask = cv2.threshold(mask,1,255,cv2.THRESH_BINARY)
         # mask = cv2.erode(mask, np.ones((1, 1),np.uint8))
         mask = cv2.dilate(mask, np.ones((2, 2),np.uint8))
         return mask

    def find_name_imgs(self, img):
        img = self.crop_image(img)
        imgs = self.crop_by_empty_rows(img)
        return list(map(self.crop_image, imgs))

    def crop_image(self, img):
        x,y,w,h = cv2.boundingRect(img)
        return img[y:y+h, x:x+w]

    def separate_images(self, img, fx):
        ans = []
        imgs = fx(img)
        while len(imgs) == 2:
            ans.append(imgs[0])
            imgs = fx(imgs[1])
        ans.append(imgs[0])
        return ans

    def crop_by_empty_rows(self, img):
        return self.separate_images(img, self.crop_by_empty_row)

    def crop_by_empty_row(self, img):
        first_row_empty = None
        for i in range(img.shape[0]): # rows
            row_is_empty = len([j for j in range(img.shape[1]) if img[i][j] > 0]) == 0
            if first_row_empty == None:
                if row_is_empty:
                    first_row_empty = i
            elif not row_is_empty:
                return [img[:first_row_empty, :], img[i:, :]]

        if first_row_empty == None:
            return [img]
        else:
            # Should never happen.
            print('Something really bad happened. Please fix.')
            return [img[:first_row_empty, :]]

    def separate_letters(self, img):
        return self.separate_images(img, self.separate_letter)

    # TODO: Make this and crop_by_empty_row generic.
    def separate_letter(self, img):
        first_col_empty = None
        for i in range(img.shape[1]):
            col_is_empty = len([j for j in range(img.shape[0]) if img[j][i] > 0]) == 0
            if first_col_empty == None:
                if col_is_empty:
                    first_col_empty = i
            elif not col_is_empty:
                return [img[:, :first_col_empty], img[:, i:]]

        if first_col_empty == None:
            return [img]
        else:
            # Should never happen.
            print('Something really bad happened. Please fix. :)')
            return [img[:, :first_col_empty]]


    # Not implemented yet, future optimization
    def find_names_color(self):
        screen = self.vision.frame
        # Get a small square on the bottom left, compare with names_color, assign
        # the color that is the closest.
        # Or use OCR to find the place of the words and then check the color there.

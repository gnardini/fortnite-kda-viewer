import numpy as np
import time
import cv2
from PIL import Image
import os
import random

class GameScreen:
    def __init__(self, vision, letters_classifier):
        self.vision = vision
        self.letters_classifier = letters_classifier

        self.enemy_color_min = [50, 65, 200]
        self.enemy_color_max = [70, 80, 255]
        self.player_kill_min = [100, 180, 40]
        self.player_kill_max = [120, 210, 55]
        self.player_death_min = [25, 75, 140]
        self.player_death_max = [40, 135, 255]
        self.white_text_min = [180, 180, 180]
        self.white_text_max = [255, 255, 255]

    def find_players(self, print_mask=False, save_letters=False, file_name=None):
        screen = self.vision.frame
        shape = screen.shape

        height = shape[0]//4
        rect = screen[(shape[0]-height*3//2):shape[0]-height//2, 0:shape[1]//4]

        other_names_mask = self.apply_mask(rect, self.enemy_color_min, self.enemy_color_max)
        other_players = self.find_name_imgs(other_names_mask)
        players = self.player_names_from_img(other_players)

        player_kill_mask = self.apply_mask(rect, self.player_kill_min, self.player_kill_max)
        player_kill = self.find_name_imgs(player_kill_mask)
        player_kill = self.player_names_from_img(player_kill)

        player_death_mask = self.apply_mask(rect, self.player_death_min, self.player_death_max)
        player_death = self.find_name_imgs(player_death_mask)
        player_death = self.player_names_from_img(player_death)

        white_text_mask = self.apply_mask(rect, self.white_text_min, self.white_text_max, is_white = True)
        white_text_imgs = self.find_name_imgs(white_text_mask)
        white_text = self.player_names_from_img(white_text_imgs, is_white = True, include_unknown = True)


        if save_letters:
            self.save_letters_to_file(other_players, file_name)

        if print_mask:
            for i in range(len(white_text_imgs)):
                print(self.player_names_from_img([white_text_imgs[i]], is_white = True, include_unknown = True))
                cv2.imshow('image', white_text_imgs[i])
                cv2.waitKey(0)
            cv2.destroyAllWindows()

        return (players, white_text)

    def apply_mask(self, img, min, max, is_white=False):
         mask = cv2.inRange(img, np.array(min, dtype=np.uint8),
               np.array(max, dtype=np.uint8))
         mask = cv2.bitwise_and(img, img, mask = mask)
         mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)

         ignore,mask = cv2.threshold(mask,1,255,cv2.THRESH_BINARY)

         if is_white:
             mask = cv2.dilate(mask, np.ones((2, 2),np.uint8))
             mask = cv2.erode(mask, np.ones((2, 2),np.uint8))
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
        diffs = []
        (imgs, diff) = fx(img)
        while len(imgs) == 2:
            ans.append(imgs[0])
            diffs.append(diff)
            (imgs, diff) = fx(imgs[1])
        ans.append(imgs[0])
        return (ans, diffs)

    def crop_by_empty_rows(self, img):
        return self.separate_images(img, self.crop_by_empty_row)[0]

    def crop_by_empty_row(self, img):
        max_consecutive_empty = 3
        consecutive_empty = 0
        first_row_empty = None
        for i in range(img.shape[0]): # rows
            row_is_empty = len([j for j in range(img.shape[1]) if img[i][j] > 0]) == 0
            if row_is_empty:
                consecutive_empty = consecutive_empty + 1
                if first_row_empty == None:
                    first_row_empty = i
            elif consecutive_empty >= max_consecutive_empty:
                return ([img[:first_row_empty, :], img[i:, :]], consecutive_empty)
            else:
                consecutive_empty = 0
                first_row_empty = None

        if first_row_empty == None:
            return ([img], 0)
        else:
            # Should never happen.
            print('Something really bad happened. Please fix.')
            return [img[:first_row_empty, :]]

    def separate_letters(self, img):
        (letters, diffs) = self.separate_images(img, self.separate_letter)
        return ([self.crop_image(l) for l in letters], diffs)

    # TODO: Make this and crop_by_empty_row generic.
    def separate_letter(self, img):
        first_col_empty = None
        for i in range(img.shape[1]):
            col_is_empty = len([j for j in range(img.shape[0]) if img[j][i] > 0]) == 0
            if first_col_empty == None:
                if col_is_empty:
                    first_col_empty = i
            elif not col_is_empty:
                return ([img[:, :first_col_empty], img[:, i:]], i - first_col_empty)

        if first_col_empty == None:
            return ([img], 0)
        else:
            # Should never happen.
            print('Something really bad happened. Please fix. :)')
            return ([img[:, :first_col_empty]], 0)

    def player_names_from_img(self, player_imgs, is_white=False, include_unknown=False):
        players = []
        for player_img in player_imgs:
            (letters, diffs) = self.separate_letters(player_img)
            letters = [self.letter_from_img(img, is_white) for img in letters]
            # Add spaces if too separated.
            final_letters = [letters[0]]
            for i in range(1, len(letters)):
                if diffs[i-1] >= 6:
                    final_letters.append(' ')
                final_letters.append(letters[i])
            player_name = ''.join(final_letters)
            if include_unknown or '?' not in player_name:
                players.append(player_name)

        return players

    def letter_from_img(self, img, is_white=False):
        letter = self.letters_classifier.classify_letter(img, is_white = is_white)
        if (letter[0] == None):
            return '?'
        return letter[0]

    def save_letters_to_file(self, name_images, file_name):
        last_index = 1
        for img in name_images:
            (letters, diffs) = self.separate_letters(img)
            for letter in letters:
                path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/dataset/screenshots/' + file_name + '-' + str(last_index) + '.png'
                cv2.imwrite(path, letter)
                last_index = last_index + 1

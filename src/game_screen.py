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
        other_players_imgs = self.find_word_imgs(other_names_mask)
        other_players = self.text_from_imgs_info(other_players_imgs)

        player_kill_mask = self.apply_mask(rect, self.player_kill_min, self.player_kill_max)
        player_kill_imgs = self.find_word_imgs(player_kill_mask)
        # TODO: Don't need the following line every screenshot. Info is always the same.
        player_kills = self.text_from_imgs_info(player_kill_imgs)

        player_death_mask = self.apply_mask(rect, self.player_death_min, self.player_death_max)
        player_death_imgs = self.find_word_imgs(player_death_mask)
        player_deaths_info = self.text_from_imgs_info(player_death_imgs)

        white_text_mask = self.apply_mask(rect, self.white_text_min, self.white_text_max, is_white = True)
        white_text_imgs = self.find_word_imgs(white_text_mask)
        white_text = self.text_from_imgs_info(white_text_imgs, is_white = True)
        white_players = [(self.player_from_white_text(text_info[0]), text_info[1]) for text_info in  white_text]
        white_players = list(filter(lambda player_info: player_info[0] != None, white_players))


        player_kills = self.find_kills(player_kills, other_players)
        player_deaths = self.find_kills(white_players, player_deaths_info)
        other_kills = self.find_kills(white_players, other_players)

        if save_letters:
            # i = self.save_letters_to_file(other_players_imgs, file_name)
            # i = self.save_letters_to_file(player_kill_imgs, file_name, current_index = i)
            # self.save_letters_to_file(player_death_imgs, file_name, current_index = i)
            self.save_letters_to_file(white_text_imgs, file_name)

        if print_mask:
            print('PRINT_MASK: %s' % white_text)
            cv2.imshow('image', white_text_mask)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # print('--------------')
        # print('Player kills: %s' % player_kills)
        # print('Player kills: %s' % player_deaths)
        # print('Other players: %s' % other_players)
        print('White players: %s' % white_text)
        # print('--------------')

        return {
            'player_kills': player_kills,
            'player_deaths': player_deaths,
            'other_kills': other_kills
        }

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

    def find_word_imgs(self, img):
        (img, y) = self.crop_image(img)
        imgs_info = self.crop_by_empty_rows(img, y)
        return list(map(lambda img_info: self.crop_image(*img_info), imgs_info))

    def crop_image(self, img, prev_y=0):
        x,y,w,h = cv2.boundingRect(img)
        return (img[y:y+h, x:x+w], y+prev_y)

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

    # Returns a list of tuples: [(img, y_height)]
    def crop_by_empty_rows(self, img, y):
        (imgs, diffs) = self.separate_images(img, self.crop_by_empty_row)
        rows_info = []
        rows_info.append((imgs[0], y))
        for i in range(1, len(imgs)):
            # Y diff of previous img + height of previous img + distance between imgs.
            rows_info.append((imgs[i], rows_info[-1][1] + imgs[i-1].shape[0] + diffs[i-1]))
        return rows_info

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
        return ([self.crop_image(l)[0] for l in letters], diffs)

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

    # Returns a list of tuples of the type (text, y_height)
    def text_from_imgs_info(self, imgs_info, is_white=False, include_unknown=True, log=False):
        players = []
        for img_info in imgs_info:
            (letters, diffs) = self.separate_letters(img_info[0])
            letters = [self.letter_from_img(img, is_white, log=log) for img in letters]
            # Add spaces if too separated.
            final_letters = [letters[0]]
            for i in range(1, len(letters)):
                if diffs[i-1] >= 6:
                    final_letters.append(' ')
                final_letters.append(letters[i])
            player_name = ''.join(final_letters)
            if include_unknown or '?' not in player_name:
                players.append((player_name, img_info[1]))

        return players

    def player_from_white_text(self, text):
        eliminated_words = ['shotgunned', 'bludgeoned', 'nearly.sploded', 'sploded', 'sniped', 'knocked out',
            'finally eliminated', 'finallyeliminated', 'eliminated', 'nearly cleared out']
        for eliminated_word in eliminated_words:
            index = text.find(eliminated_word)
            if index >= 3:
                return text[:index-1]
        return None

    def letter_from_img(self, img, is_white=False, log=False):
        letter = self.letters_classifier.classify_letter(img, is_white = is_white, log=log)
        if (letter[0] == None):
            return '?'
        return letter[0]

    def save_letters_to_file(self, images_info, file_name, current_index = 1):
        name_images = [image_info[0] for image_info in images_info]
        for img in name_images:
            (letters, diffs) = self.separate_letters(img)
            for letter in letters:
                path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/dataset/screenshots/' + file_name + '-' + str(current_index) + '.png'
                cv2.imwrite(path, letter)
                current_index = current_index + 1
        return current_index

    def find_kills(self, killer_players, dead_players):
        matching = []
        for (killer_player, killer_y) in killer_players:
            for (dead_player, dead_y) in dead_players:
                if (abs(killer_y - dead_y) < 10):
                    matching.append((killer_player, dead_player))
        return matching

import numpy as np
import cv2
import json
import os
from operator import mul
import string

class LettersClassifier:

    def __init__(self):
        path = os.path.join(os.path.split(os.path.split(__file__)[0])[0], 'dataset')
        screenshots_path = os.path.join(path, 'screenshots')
        with open(os.path.join(path,'mapping.json')) as f:
            json_data = f.read()
            self.mapping = json.loads(json_data)
            self.mapping_images = self.load_images(self.mapping, screenshots_path)
        with open(os.path.join(path,'white_mapping.json')) as f:
            json_data = f.read()
            self.white_mapping = json.loads(json_data)
            self.white_mapping_images = self.load_images(self.white_mapping, os.path.join(screenshots_path, 'white'))
        self.max_threshold = .02
        self.most_used_letters = ['a', 'e', 'i', 'o', 'u', 'n', 's', 'r', 'h', 'l', 'm']
        self.most_used_letters = self.most_used_letters + [letter.upper() for letter in self.most_used_letters]
        self.common_letters = [key for key in self.most_used_letters if key in self.mapping.keys()]
        self.common_white_letters = [key for key in self.most_used_letters if key in self.white_mapping.keys()]
        self.uncommon_letters = [key for key in self.mapping.keys() if key not in self.most_used_letters]
        self.uncommon_white_letters = [key for key in self.white_mapping.keys() if key not in self.most_used_letters]

    def classify_letter(self, img, is_white=False, mapping=None, log=False):
        if is_white:
            mapping = self.white_mapping
            imgs_mapping = self.white_mapping_images
            common_letters = self.common_white_letters
            uncommon_letters = self.uncommon_white_letters
        else:
            mapping = self.mapping
            imgs_mapping = self.mapping_images
            common_letters = self.common_letters
            uncommon_letters = self.uncommon_letters

        (letter, lowest_dist) = self.find_best_letter(img, common_letters, mapping, imgs_mapping, log)
        if lowest_dist < self.max_threshold:
            return (letter, lowest_dist)
        other_letter, dist = self.find_best_letter(img, uncommon_letters, mapping, imgs_mapping, log)
        if dist < lowest_dist:
            lowest_dist = dist
            letter = other_letter

        return (letter, lowest_dist)

    def find_best_letter(self, img, letters, mapping, img_mapping, log=False):
        letter = None
        lowest_dist = 1
        for k in letters:
            dist = self.find_lowest_distance(img, mapping, img_mapping, k, log)
            if dist < lowest_dist:
                if dist < self.max_threshold:
                    return (k, dist)
                lowest_dist = dist
                letter = k
        return (letter, lowest_dist)

    def find_lowest_distance(self, img, mapping, img_mapping, letter, log=False):
        min = 1
        for file in mapping[letter]:
            other_img = img_mapping[file]
            dist = self.images_distance(img, other_img)
            # Just searching for a letter, feel free to fix this log.
            if log and (dist < .1 or (dist < 1 and letter == 'i')):
                print('Distance from %s: %f' % (letter, dist))
            if dist < min:
                min = dist
        return min

    def images_distance(self, img1, img2):
        shape1 = img1.shape
        shape2 = img2.shape

        if shape1 == shape2:
            return self.equal_images_distance(img1, img2)
        elif abs(shape1[0] - shape2[0]) > 2 or abs(shape1[1] - shape2[1]) > 2:
            return 1.
        else:
            combinations = self.combine_widths(img1, img2)
            combinations = [self.combine_heights(*combination) for combination in combinations]
            combinations = [item for sublist in combinations for item in sublist]
            return min(list(map(lambda combination: self.equal_images_distance(*combination), combinations)))


    def equal_images_distance(self, img1, img2):
        if img1.shape != img2.shape:
            raise ValueError('Shapes are not equal: ' + str(img1.shape) + ' ' + str(img2.shape))
        different = cv2.bitwise_xor(img1, img2)
        different_bits = np.count_nonzero(different)
        return different_bits / (img1.shape[0] * img1.shape[1])

    def combine_widths(self, img1, img2):
        shape1 = img1.shape
        shape2 = img2.shape
        diff = shape1[1] - shape2[1]
        if diff < 0:
            diff = -diff
            aux = img1
            img1 = img2
            img2 = aux
            shape1 = img1.shape
            shape2 = img2.shape

        combinations = []
        if diff == 0:
            combinations.append((img1, img2))

        if diff == 2:
            new_shape = (img2.shape[0], img2.shape[1] + 2)
            two_left = np.zeros(new_shape, img1.dtype)
            one_and_one = np.zeros(new_shape, img1.dtype)
            two_right = np.zeros(new_shape, img1.dtype)

            two_left[:, 2:] = img2
            one_and_one[:, 1:-1] = img2
            two_right[:, :-2] = img2
            combinations.append((img1, two_left))
            combinations.append((img1, one_and_one))
            combinations.append((img1, two_right))
        elif diff == 1:
            new_shape = (img2.shape[0], img2.shape[1] + 1)
            left = np.zeros(new_shape, img1.dtype)
            right = np.zeros(new_shape, img1.dtype)

            left[:, 1:] = img2
            right[:, :-1] = img2
            combinations.append((img1, left))
            combinations.append((img1, right))

        return combinations

    def combine_heights(self, img1, img2):
        shape1 = img1.shape
        shape2 = img2.shape
        diff = shape1[0] - shape2[0]
        if diff < 0:
            diff = -diff
            aux = img1
            img1 = img2
            img2 = aux
            shape1 = img1.shape
            shape2 = img2.shape

        combinations = []
        if diff == 0:
            combinations.append((img1, img2))

        if diff == 2:
            two_top = np.zeros(img1.shape, img1.dtype)
            one_and_one = np.zeros(img1.shape, img1.dtype)
            two_down = np.zeros(img1.shape, img1.dtype)

            two_top[2:, :] = img2
            one_and_one[1:-1, :] = img2
            two_down[:-2, :] = img2
            combinations.append((img1, two_top))
            combinations.append((img1, one_and_one))
            combinations.append((img1, two_down))
        elif diff == 1:
            top = np.zeros(img1.shape, img1.dtype)
            down = np.zeros(img1.shape, img1.dtype)

            top[1:, :] = img2
            down[:-1, :] = img2
            combinations.append((img1, top))
            combinations.append((img1, down))


        return combinations

    def load_images(self, mapping, path):
        images = {}
        for letter in mapping:
            for file in mapping[letter]:
                images[file] = cv2.imread(os.path.join(path, file), 0)
        return images

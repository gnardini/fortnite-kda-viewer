import numpy as np
import cv2
import json

class LettersClassifier:

    def __init__(self):
        self.path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/dataset/'
        json_data = open(self.path + 'mapping.json').read()
        self.mapping = json.loads(json_data)

        self.max_threshold = .05

    def classify_letter(self, img, mapping=None):
        if mapping == None:
            mapping = self.mapping
        min = 1
        letter = None
        for k in mapping:
            for file in mapping[k]:
                other_img = cv2.imread(self.path + 'screenshots/' + file)
                dist = self.images_distance(img, other_img)
                if dist < min:
                    min = dist
                    letter = k
        return (letter, min)

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
        return different_bits / (img1.shape[0] * img1.shape[1] * img1.shape[2])

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
            new_shape = (img2.shape[0], img2.shape[1] + 2, img2.shape[2])
            two_left = np.zeros(new_shape, img1.dtype)
            one_and_one = np.zeros(new_shape, img1.dtype)
            two_right = np.zeros(new_shape, img1.dtype)

            two_left[:, 2:, :] = img2
            one_and_one[:, 1:-1, :] = img2
            two_right[:, :-2, :] = img2
            combinations.append((img1, two_left))
            combinations.append((img1, one_and_one))
            combinations.append((img1, two_right))
        elif diff == 1:
            new_shape = (img2.shape[0], img2.shape[1] + 1, img2.shape[2])
            left = np.zeros(new_shape, img1.dtype)
            right = np.zeros(new_shape, img1.dtype)

            left[:, 1:, :] = img2
            right[:, :-1, :] = img2
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

            two_top[2:, :, :] = img2
            one_and_one[1:-1, :, :] = img2
            two_down[:-2, :, :] = img2
            combinations.append((img1, two_top))
            combinations.append((img1, one_and_one))
            combinations.append((img1, two_down))
        elif diff == 1:
            top = np.zeros(img1.shape, img1.dtype)
            down = np.zeros(img1.shape, img1.dtype)

            top[1:, :, :] = img2
            down[:-1, :, :] = img2
            combinations.append((img1, top))
            combinations.append((img1, down))


        return combinations

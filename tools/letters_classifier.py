import os
import cv2
import json
import numpy as np
from src import letters_classifier

path = os.path.join(os.path.split(os.path.split(__file__)[0])[0], "dataset")


json_data = open(os.path.join(path, 'mapping.json')).read()
mapping = json.loads(json_data)

classifier = letters_classifier.LettersClassifier()

first = '0'
second = 'O'

for e_file in mapping[first]:
    e_img = cv2.imread(os.path.join(path, 'screenshots', e_file))
    for e_file2 in mapping[first]:
        e_img2 = cv2.imread(os.path.join(path, 'screenshots',  e_file2))
        print(first + ': ' + str(classifier.images_distance(e_img, e_img2)))
    for u_file in mapping[second]:
        u_img = cv2.imread(os.path.join(path, 'screenshots', u_file))
        print(second + ': ' + str(classifier.images_distance(e_img, u_img)))

# sizes = {}
# for k in mapping:
#     print('-----------------')
#     print(k)
#     for file in mapping[k]:
#         img = cv2.imread(path + 'screenshots/' + file)
#         print('h: ' + str(img.shape[0]) + ' w:' + str(img.shape[1]) + ' ' + file)

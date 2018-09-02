import os
import cv2
import json
import numpy as np

path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/dataset/'


json_data = open(path + 'white_mapping.json').read()
mapping = json.loads(json_data)
cv2.namedWindow('image')

letter = 'h'
for file in mapping[letter]:
    img = cv2.imread(path + 'screenshots/white/' + file, 0)
    cv2.imshow('image', img)
    cv2.waitKey(0)

cv2.destroyAllWindows()

import os
import sys
import cv2
import json
import numpy as np

path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/dataset/'

letter = 'p'
if len(sys.argv) > 1:
    letter = sys.argv[1]

json_data = open(path + 'mapping.json').read()
mapping = json.loads(json_data)
cv2.namedWindow('image')


for file in mapping[letter]:
    img = cv2.imread(path + 'screenshots/' + file, 0)
    bordersize = 3
    img = cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[0])
    cv2.imshow('image', img)
    cv2.waitKey(0)

cv2.destroyAllWindows()

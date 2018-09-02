import os
import cv2
import json

path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/dataset/'


json_data = open(path + 'mapping.json').read()
mapping = json.loads(json_data)

sizes = {}
for k in mapping:
    print('-----------------')
    print(k)
    for file in mapping[k]:
        img = cv2.imread(path + 'screenshots/' + file)
        print('w: ' + str(img.shape[0]) + ' h:' + str(img.shape[1]) + ' ' + file)

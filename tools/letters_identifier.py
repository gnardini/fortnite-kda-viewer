import os
import cv2
import json
from pprint import pprint

path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/dataset/'


json_data = open(path + 'mapping.json').read()
mapping = json.loads(json_data)
parsed_files = []
for k in mapping:
    parsed_files = parsed_files + mapping[k]

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

used = []
for file in os.listdir(path):
    if not file.endswith('.json') and not file in parsed_files:
        img = cv2.imread(path + file)
        bordersize = 3
        border = cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])
        cv2.imshow('image', border)
        character = chr(cv2.waitKey(0))
        while character == '/':
            to_delete = used.pop()
            deleted = mapping[to_delete].pop()
            print('Delted file %s from letter %s' % (deleted, to_delete))
            character = chr(cv2.waitKey(0))
        print(character)
        if character == '.':
            break
        elif character == ',':
            continue
        else:
            used.append(character)
            if not character in mapping:
                mapping[character] = []
            mapping[character].append(file)

with open(path + 'mapping.json', 'w') as outfile:
    json.dump(mapping, outfile, indent=4, sort_keys=True)
cv2.destroyAllWindows()

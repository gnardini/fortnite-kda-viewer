import os
import cv2
import json
from src import letters_classifier

white_mapping = True
path = os.path.join(os.path.split(os.path.split(__file__)[0])[0], "dataset")
screenshots_dir = 'screenshots'
mapping_file = 'mapping.json'
if white_mapping:
    mapping_file = 'white_mapping.json'
    screenshots_dir = os.path.join(screenshots_dir, 'white')

json_data = open(os.path.join(path, mapping_file)).read()
mapping = json.loads(json_data)
classifier = letters_classifier.LettersClassifier()
parsed_files = []
for k in mapping:
    parsed_files = parsed_files + mapping[k]

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

used = []
for file in os.listdir(os.path.join(path, screenshots_dir)):
    if not file.endswith('.json')  and not file.endswith('white') and not file in parsed_files:
        file_path = os.path.join(path, screenshots_dir, file)
        img = cv2.imread(file_path, 0)
        if (img is None or img.shape == None):
            os.remove(file_path)
            continue
        print(file)
        letter = classifier.classify_letter(img, mapping = mapping, is_white = white_mapping)
        if letter[1] <= .03:
            print('Found a ' + letter[0] + ' with error ' + str(letter[1]))
            os.remove(file_path)
            continue
        bordersize = 3
        border = cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[0])
        cv2.imshow('image', border)

        val = cv2.waitKey(0)
        if val == 13: # 13 is enter key.
            buffer = []
            val = 0
            while True:
                val = cv2.waitKey(0)
                if val == 13:
                    break
                buffer.append(chr(val))
            character = ''.join(buffer)
        elif val == 127: # Backspace key.
            print('Removing file %s' % file)
            os.remove(file_path)
            continue
        else:
            character = chr(val)
        print(character)
        while character == '/':
            to_delete = used.pop()
            deleted = mapping[to_delete].pop()
            print('Removed file %s from letter %s' % (deleted, to_delete))
            character = chr(cv2.waitKey(0))
        print(character)
        if character == '*':
            break
        elif character == ',':
            continue
        else:
            used.append(character)
            if not character in mapping:
                mapping[character] = []
            mapping[character].append(file)

with open(os.path.join(path, mapping_file), 'w') as outfile:
    json.dump(mapping, outfile, indent=4, sort_keys=True)
cv2.destroyAllWindows()

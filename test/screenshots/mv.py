import os

path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/test/screenshots'

i=7
for file in os.listdir(path + '/snap'):
    os.rename(path + '/snap/' + file, path + '/screenshot' + str(i) + '.png')
    i =i +1

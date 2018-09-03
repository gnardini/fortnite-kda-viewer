import os

path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/test/screenshots'

i=40
for file in os.listdir(path + '/snaps'):
    os.rename(path + '/snaps/' + file, path + '/screenshot' + str(i) + '.png')
    i =i +1

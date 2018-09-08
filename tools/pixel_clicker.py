import cv2
import numpy as np

path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/test/screenshots/screenshot77.png'

img = cv2.imread(path)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
shape = img.shape
height = shape[0]//4
img = img[(shape[0]-height*3//2):shape[0]-height//2, 0:shape[1]//4]

px = np.zeros((100,100,3), np.uint8)

def read_pixel(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(img[y, x])
        px[:, :] = img[y, x]
        cv2.imshow('pixel', px)

cv2.namedWindow('pixel')

cv2.namedWindow('image')
cv2.setMouseCallback('image', read_pixel)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

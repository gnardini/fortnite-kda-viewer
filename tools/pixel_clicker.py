import cv2

path = '/Users/gnardini/Documents/Code/fortnite-kda-viewer/test/screenshots/screenshot.png'

img = cv2.imread(path)
shape = img.shape
height = shape[0]//4
img = img[(shape[0]-height*3//2):shape[0]-height//2, 0:shape[1]//4]

def read_pixel(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(img[y, x])

cv2.namedWindow('image')
cv2.setMouseCallback('image', read_pixel)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

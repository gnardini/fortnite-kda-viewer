import cv2
from mss import mss
from PIL import Image
import numpy as np
import cv2

class Vision:
    def __init__(self):
        self.monitor = {'top': 800, 'left': 0, 'width': 460, 'height': 150}
        self.screen = mss()

        self.frame = None

    def refresh_frame(self):
        self.frame = self.take_screenshot()

    def convert_rgb_to_bgr(self, img):
        return img[:, :, ::-1]

    # Improve this. Size should not be an input value (monitor).
    def take_screenshot(self):
        screeshot_img = self.screen.grab(self.monitor)
        img = Image.frombytes('RGB', screeshot_img.size, screeshot_img.rgb)
        img = np.array(img)
        if img.shape[0] == 2 * self.monitor['height']:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

        img = self.convert_rgb_to_bgr(img)
        return img

    def save_frame(self):
        path = os.path.join(os.path.split(os.path.split(__file__)[0])[0], 'out')
        cv2.imwrite(path, self.frame[800:950, :460, :])

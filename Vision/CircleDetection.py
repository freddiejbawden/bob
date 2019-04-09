import cv2
import numpy as np
from matplotlib import pyplot as plt


class CircleDetection:
    background_colour = 255

    # Change colour to match illumination
    def normalise_rgb(self, target_colour):
        return self.background_colour * (target_colour / 255.0)

    def detect_blue(self, image):
        # Isolate the colour in the image as a binary image
        #colour = self.normalise_rgb(255)
        #lower_limit = colour - 100
        #upper_limit = colour + 100

        # define range of blue color in HSV
        lower_blue = np.array([30, 50, 50])
        upper_blue = np.array([50, 255, 255])

        #mask = cv2.inRange(image, (lower_limit, 0, 0), (upper_limit, 100, 100))
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(image, lower_blue, upper_blue)
        # detecting centre of circle

        kernel = np.ones((5, 5), np.uint8)
        # This applies a dilate that makes the binary region larger (the more iterations the larger it becomes)
        mask = cv2.dilate(mask, kernel, iterations=10)
        # erode to remove noise
        mask = cv2.erode(mask, kernel, iterations=10)

        cv2.imshow("circle", mask)
        cv2.waitKey(0)

        # Obtain the contours of the binary image
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        try:
            (x, y), radius = cv2.minEnclosingCircle(contours[0])
        except:
            (x, y) = (0, 0)

        return mask, np.array([x, y])

    def match_template(self, img):
        template = cv2.imread('star2.jpg', 0)
        img2 = img.copy()
        w, h = template.shape[::-1]

        method = eval('cv2.TM_CCORR')



        # Apply template Matching
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img, top_left, bottom_right, 255, 2)
        plt.subplot(121), plt.imshow(res, cmap='gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img, cmap='gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.show()

        #cv2.imshow("bob", template)
        #cv2.waitKey(0)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    #cap.set(10, 100); # brightness
    #cap.set(11, 100); # contrast
    #cap.set(12, 100); # saturation
    circle_detector = CircleDetection()

    for i in range(50):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # frame dimensions 480 X 640 X 3

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print("HSV {} BGR {}".format(frame_hsv[479][639], frame[479][639]))
        # cv2.imshow("frame", frame)
        #cv2.waitKey(0)

        circle_detector.match_template(frame_grey)
        #mask, coordinates = circle_detector.detect_blue(frame_hsv)

        #cv2.imshow("circle", mask)
        #cv2.waitKey(0)

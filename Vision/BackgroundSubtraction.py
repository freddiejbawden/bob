import numpy as np
import cv2

cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Range for blue
    lower_blue = np.array([200/2., 120, 70])
    upper_blue = np.array([270/2., 255, 255])
    mask1 = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((5, 5), np.uint8)
    # This applies a dilate that makes the binary region larger (the more iterations the larger it becomes)
    mask1 = cv2.dilate(mask1, kernel, iterations=5)
    # erode to remove noise
    mask1 = cv2.erode(mask1, kernel, iterations=5)

    # Range for black
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])
    mask2 = cv2.inRange(hsv, lower_black, upper_black)
    kernel = np.ones((5, 5), np.uint8)
    # This applies a dilate that makes the binary region larger (the more iterations the larger it becomes)
    #mask2 = cv2.dilate(mask2, kernel, iterations=5)
    # erode to remove noise
    #mask2 = cv2.erode(mask2, kernel, iterations=5)

    #fgmask = fgbg.apply(frame)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.waitKey(1)
    cv2.imshow('game', mask1)
    cv2.waitKey(1)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
     #   break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

#! /usr/bin/env python3
import cv2
import numpy as np

def centre_detection():
    cap = cv2.VideoCapture(0)
    cap_width = int(cap.get(3))
    cap_height = int(cap.get(4))
    OBJECT_THRESHOLD = 0.08 # proportion of area that has to be filled

    # Capture frame-by-frame
    ret, frame = cap.read()
    edges = cv2.Canny(frame,100,200)


    kernel = np.ones((5, 5), np.uint8)
    # This applies a dilate that makes the binary region larger (the more iterations the larger it becomes)
    mask = cv2.dilate(edges, kernel, iterations=5)
    mask_copy = mask.copy()


    #cv2.imshow('frame', frame)
    #cv2.waitKey(1)
    #cv2.imshow('edges', edges)
    #cv2.waitKey(1)
    #cv2.imshow('mask', mask)
    #cv2.waitKey(1)

    # Find contours
    contours, _ = cv2.findContours(mask_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        # find the biggest area
        obj = max(contours, key=cv2.contourArea)
        centre = np.reshape(np.mean(obj, 0, dtype=np.int), 2)
    else:
        print('no object visible')
        return('empty')

    #print(centre)
    area = cv2.contourArea(obj)

    pixels = np.ones((cap_width, cap_height))
    print('area:', area)
    #print('big yeet:', np.sum(pixels))
    print('threshold:', OBJECT_THRESHOLD * (np.sum(pixels)))

    if area > OBJECT_THRESHOLD*(np.sum(pixels)):
        if centre[0] < cap_width*1/4:
            print('left')
            return('left')
        elif centre[0] > cap_width*3/4:
            print('right')
            return('right')
        else:
            print('centre')
            return('centre')
    else:
        print('below threshold')
        return('empty')

#if __name__ == "__main__":
#    for i in range(5000):
#        print(centre_detection())





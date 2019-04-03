import cv2
import numpy as np

# https://thecodacus.com/object-recognition-using-opencv-python/#.XJ55xJzgoeM
# http://jematoscv.blogspot.com/2014/05/matching-features-with-orb-using-opencv.html

detector = cv2.ORB() #FeatureDetector_create("ORB")#cv2.xfeatures2d.SIFT_create() #cv2.SIFT()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

#trainImg=cv2.imread("sweep.jpg")
trainImg=cv2.imread("star.png")
gray = cv2.cvtColor(trainImg, cv2.COLOR_BGR2GRAY)
trainKP, trainDesc = detector.detectAndCompute(trainImg, None)

cam=cv2.VideoCapture(0)
width = cam.get(3)
height = cam.get(4)
cam.set(3, width/2)
cam.set(4, height/2)

while True:
    ret, QueryImgBGR = cam.read()
    queryImg = cv2.cvtColor(QueryImgBGR, cv2.COLOR_BGR2GRAY)
    queryKP, queryDesc = detector.detectAndCompute(queryImg, None)

    matches = bf.match(queryDesc,trainDesc)
    dist = [m.distance for m in matches]
    try:
        thres_dist = (sum(dist) / len(dist)) * 0.5
    except:
        thresh_dist = 0
    goodMatch = [m for m in matches if m.distance < thres_dist]

    MIN_MATCH_COUNT = 7
    if len(goodMatch) >= MIN_MATCH_COUNT:
        print "Matches found- %d/%d" % (len(goodMatch), MIN_MATCH_COUNT)
        tp = []
        qp = []

        for m in goodMatch:
            tp.append(trainKP[m.trainIdx].pt)
            qp.append(queryKP[m.queryIdx].pt)

        tp, qp = np.float32((tp, qp))

        H, status = cv2.findHomography(tp, qp, cv2.RANSAC, 3.0)

        h, w, c = trainImg.shape
        trainBorder = np.float32([[[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]])
        queryBorder = cv2.perspectiveTransform(trainBorder, H)
        cv2.polylines(QueryImgBGR, [np.int32(queryBorder)], True, (0, 255, 0), 5)
    else:
        print "Not Enough match found- %d/%d"%(len(goodMatch), MIN_MATCH_COUNT)
    cv2.imshow('result', QueryImgBGR)
    if cv2.waitKey(10) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

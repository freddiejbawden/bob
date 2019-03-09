import cv2
import numpy as np

def objectDetect(image):
	kernel = np.ones((5,5),np.uint8)
	thresh=peakPick(image)
	print(thresh)
	img_bin = abs(threshold(image, thresh)-1)
	# convert to 0-255 range
	img_bin = np.array(img_bin, dtype=np.uint8)*255

	# Erode to remove noise
	# more iterations, less noise but slower
	img_bin = cv2.erode(img_bin, kernel, iterations=1)
	# Dilate increases size to reduce number of lost pixels
	img_bin = cv2.dilate(img_bin, kernel, iterations=4)
	# Erode again to remove connections
	img_bin = cv2.erode(img_bin, kernel, iterations=8)

	# Find contours
	_,contours,_ = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# Centre of largest contour
	obj = contours[0]
	centre = np.reshape(np.mean(obj,0,dtype=np.int),2)

	cv2.imshow("object contour",img_bin)
	cv2.waitKey(0)

	# Find bounding size by moving until pixel is 0
	# Image is not symmetrical so have to go in all directions
	right = boundValue(img_bin[centre[1],:], centre[0], 1)
	left = boundValue(img_bin[centre[1],:], centre[0], -1)
	down = boundValue(img_bin[:,centre[0]], centre[1], 1)
	up = boundValue(img_bin[:,centre[0]], centre[1], -1)
	obj_img = img_bin[up:down, left:right]
	cv2.imshow("object", obj_img)
	cv2.waitKey(0)

	for c in contours:
		img2 = cv2.drawContours(image.copy(), c, -1, 255, 3)
		cv2.imshow("Circled objects", img2)
		cv2.waitKey(0)

def peakPick(image):
	img_hist=cv2.calcHist([image],[0],None,[256],[0,256])
	# Find peak in histogram
	peak = np.argmax(img_hist)
	# Find peak in the darker side of the above peak value
	peak_darker = 1
	for i in range(1,peak):
		if img_hist[i-1] < img_hist[i] and img_hist[i] >= img_hist[i+1] and img_hist[i]>img_hist[peak_darker]:
			peak_darker=i
	# Find the deepest valley bewteen the two peaks
	# This will be our threshold value
	thresh = peak_darker+1
	for i in range(peak_darker+1,peak):
		if img_hist[i-1] > img_hist[i] and img_hist[i] <= img_hist[i+1] and img_hist[i] < img_hist[thresh]:
			thresh = i
	return thresh

def threshold(image, thresh):
	# return binary array
	image = np.array(image)
	height, width = np.shape(image)
	output = np.zeros([height, width])
	for row in range(height):
		for col in range(width):
			if image[row][col]>thresh:
				output[row][col] = 1
	return output

def boundValue(array, centre, direction):
	value = 1
	index = centre
	while value > 0:
		index += direction
		value = array[index]
	return index


def main():
	cap = cv2.VideoCapture(0)
	# Capture frame-by-frame
	ret, frame = cap.read()
    # Convert image to black and white
	grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	objectDetect(grey)
	return

if __name__ == "__main__":
    main()

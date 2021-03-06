# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 15:45:02 2019

@author: Santosh
"""
# import the necessary packages
from shapedetector import ShapeDetector
from scipy.spatial import distance as dist
import argparse
import imutils
import cv2

def detect(image):
    points = cv2.goodFeaturesToTrack(
        image,
        maxCorners=20,
        qualityLevel=0.04,
        minDistance=1.0,
        useHarrisDetector=False,
    )
 
    if points is not None and len(points) > 0:
        return [[point[0][0].item(), point[0][1].item(), 1, 1] for point in points]
 
    return None

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
 
# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]

edged = cv2.Canny(blurred, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()
# loop over the contours
for c in cnts:
    
    if cv2.contourArea(c) < 1000:
        	continue
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
    epsilon = 0.02*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    
    print(approx)
    for i in range(1, len(approx)):
        print(dist.euclidean(approx[i-1], approx[i]))
    print(dist.euclidean(approx[0], approx[-1]))
    print("Hey")
    #cv2.imwrite('Images\approx.png', approx)
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)
    shape = sd.detect(c)
 
	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 255, 255), 2)
 
	# show the output image
    cv2.imshow("Image", image)
    cv2.imwrite("late_o_o.png", image)
    cv2.waitKey(0)
#cv2.imshow("approx", approx)

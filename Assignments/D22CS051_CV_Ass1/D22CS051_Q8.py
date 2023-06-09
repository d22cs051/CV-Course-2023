# -*- coding: utf-8 -*-
"""D22CS051_Q8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17_Sas4pU204OAEeIzNi1g12sLq6w3eeD
"""

# importing libs
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

img1 = cv.imread('img_template.jpg',cv.IMREAD_GRAYSCALE) # template image
img2 = cv.imread('img_original.jpg',cv.IMREAD_GRAYSCALE) # original image

# applying thresholding
_,img1 = cv.threshold(img1,127,255,cv.THRESH_BINARY)
_,img2 = cv.threshold(img2,127,255,cv.THRESH_BINARY)

# initiate ORB detector
orb = cv.ORB_create()
# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
# match descriptors.
matches = bf.match(des1,des2)
# sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)
# draw first 10 matches.
img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
plt.figure(figsize=(15,12))
plt.imshow(img3)
plt.show()

# initiate SIFT detector
sift = cv.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# BFMatcher with default params
bf = cv.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.45*n.distance:
        good.append([m])
# cv.drawMatchesKnn expects list of lists as matches.
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
plt.figure(figsize=(15,12))
plt.imshow(img3)
plt.show()
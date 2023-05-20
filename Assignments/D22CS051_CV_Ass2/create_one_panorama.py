# -*- coding: utf-8 -*-
"""CV A2-B 3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tTSo-13C12WqV6dJm63-Vvr_44-TEh3B

# Q3: Write down steps to stitch images to create the panorama

The general steps to stitch images to create a panorama using computer vision:

Step 1: Capture Overlapping Images
The first step is to capture a set of overlapping images of the scene. The images should have some overlapping areas so that they can be stitched together.

Step 2: Detect Feature Points
Next, we need to detect feature points in each image. Feature points are distinct, identifiable points in the image, such as corners, edges, or blobs. Feature detection algorithms, such as SIFT, SURF, or ORB, can be used to detect feature points.
Note:- SURF is now pattent and can't be used for commercial uses.

Step 3: Compute Descriptors
For each feature point, we need to compute a descriptor, which is a numerical representation of the local image patch around the feature point. Descriptors capture the texture, color, and other characteristics of the image patch and are used to match feature points across different images.

Step 4: Match Feature Points
Using the computed descriptors, we can match corresponding feature points across different images. This can be done using algorithms such as nearest neighbor or RANSAC.

Step 5: Compute Homography Matrix
Once we have a set of matched feature points, we can compute a homography matrix that describes the transformation between the images. The homography matrix maps points in one image to corresponding points in the other image.

Step 6: Warp Images
Using the homography matrix, we can warp the images to align them with each other. This involves transforming the pixels of one image to the coordinate system of the other image.

Step 7: Blend Images
After warping the images, there may be areas of overlap where the pixels from both images are present. We need to blend these overlapping areas to create a seamless transition between the two images. This can be done using blending techniques such as alpha blending, gradient blending, or multi-band blending.

Step 8: Repeat for Multiple Images
Steps 2 to 7 are repeated for all pairs of adjacent images in the set. This creates a chain of aligned images that can be combined into a single panorama.

Step 9: Combine Images
Finally, the chain of aligned images is combined into a single panorama. This can be done using techniques such as image stitching or image mosaicing.

These are the general steps involved in stitching images to create a panorama using computer vision. Different implementations may use variations on these steps or additional steps to improve the accuracy and quality of the result.

## Create the panorama for the given images
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# read images and transform them to grayscale
# Make sure that the train image is the image that will be transformed
img_1 = cv.imread('1a.jpeg')
img_1_gray = cv.cvtColor(img_1, cv.COLOR_RGB2GRAY)

img_2 = cv.imread('1b.jpeg')
# Opencv defines the color channel in the order BGR. 
# Transform it to RGB to be compatible to matplotlib
img_2_gray = cv.cvtColor(img_2, cv.COLOR_RGB2GRAY)

plt.figure(figsize=(12,12))
plt.subplot(1,2,1)
plt.imshow(img_1[:,:,::-1])
plt.subplot(1,2,2)
plt.imshow(img_2[:,:,::-1])
plt.show()

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from pathlib import Path

def sift_matching_bf_knn(img1:np.array,img2:np.array)->None:
  ### Inits ###
  # Initiate SIFT detector
  sift = cv.SIFT_create()
  # find the keypoints and descriptors with SIFT
  kp1, des1 = sift.detectAndCompute(img1,None)
  kp2, des2 = sift.detectAndCompute(img2,None)
  # BFMatcher with default params
  bf = cv.BFMatcher()
  matches = bf.knnMatch(des1,des2,k=2)
  # Apply ratio test
  bf = cv.BFMatcher()
  matches = bf.knnMatch(des1,des2,k=2)
  # Apply ratio test
  good = []
  for m,n in matches:
      if m.distance < 0.7*n.distance:
          good.append(m)

  ### Applying findHomography ###
  if len(good)>=MIN_MATCH_COUNT:
      src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
      dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
      M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
      matchesMask = mask.ravel().tolist()
      h,w = img1.shape[:2]
      pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
      dst = cv.perspectiveTransform(pts,M)
      img2 = cv.polylines(img2,[np.int32(dst)],True,(255,255,255),3, cv.LINE_AA)
  else:
      print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
      matchesMask = None
    

  ### Ploting Matcheings and outline ###
  draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    matchesMask = matchesMask, # draw only inliers
                    flags = 2)
  img3 = cv.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
  plt.figure(figsize=(12,8))
  if len(img3.shape)>2:
    plt.imshow(img3[:,:,::-1], 'gray')
  else:
    plt.imshow(img3, 'gray')
  plt.show()

  return matches,M,mask

MIN_MATCH_COUNT = 50
matches, M, mask = sift_matching_bf_knn(img_1_gray,img_2_gray)
print("-------------------------------------------------------")
print(M)

# Apply panorama correction
# print(img_1.shape,img_2.shape)
width = img_1.shape[1] + img_2.shape[1]
height = img_1.shape[0] + img_2.shape[0]

result = cv.warpPerspective(img_1, M, (width, height))
result[0:img_2.shape[0], 0:img_2.shape[1]] = img_2

plt.figure(figsize=(20,10))
plt.imshow(result[:,:,::-1])

plt.axis('off')
plt.show()

import imutils
# transform the panorama image to grayscale and threshold it 
gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY)[1]

# Finds contours from the binary image
cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# get the maximum contour area
c = max(cnts, key=cv.contourArea)

# get a bbox from the contour area
(x, y, w, h) = cv.boundingRect(c)

# crop the image to the bbox coordinates
result = result[y:y + h, x:x + w]

# show the cropped image
plt.figure(figsize=(12,12))
plt.imshow(result[:,:,::-1])
plt.imsave("1a_1b.jpeg",result[:,:,::-1])
plt.show()

"""## Repeating above steps"""

# read images and transform them to grayscale
# Make sure that the train image is the image that will be transformed
img_1 = cv.imread('1a_1b.jpeg')
img_1_gray = cv.cvtColor(img_1, cv.COLOR_RGB2GRAY)

img_2 = cv.imread('1a.jpeg')
# Opencv defines the color channel in the order BGR. 
# Transform it to RGB to be compatible to matplotlib
img_2_gray = cv.cvtColor(img_2, cv.COLOR_RGB2GRAY)

plt.figure(figsize=(12,12))
plt.subplot(1,2,1)
plt.imshow(img_1[:,:,::-1])
plt.subplot(1,2,2)
plt.imshow(img_2[:,:,::-1])
plt.show()

MIN_MATCH_COUNT = 50
matches, M, mask = sift_matching_bf_knn(img_1_gray,img_2_gray)
print("-------------------------------------------------------")
print(M)

# Apply panorama correction
# print(img_1.shape,img_2.shape)
width_new = width + img_2.shape[1]
height_new = height + img_2.shape[0]

result = cv.warpPerspective(img_1, M, (width_new, height_new))
result[0:img_2.shape[0], 0:img_2.shape[1]] = img_2

plt.figure(figsize=(20,10))
plt.imshow(result[:,:,::-1])

plt.axis('off')
plt.show()

import imutils
# transform the panorama image to grayscale and threshold it 
gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY)[1]

# Finds contours from the binary image
cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# get the maximum contour area
c = max(cnts, key=cv.contourArea)

# get a bbox from the contour area
(x, y, w, h) = cv.boundingRect(c)

# crop the image to the bbox coordinates
result = result[y:y + h, x:x + w]

# show the cropped image
plt.figure(figsize=(12,12))
plt.imshow(result[:,:,::-1])
plt.imsave("1a_1b_1c.jpeg",result[:,:,::-1])
plt.show()

"""Refrences:
1. https://towardsdatascience.com/image-panorama-stitching-with-opencv-2402bde6b46c
2. https://medium.com/analytics-vidhya/panorama-formation-using-image-stitching-using-opencv-1068a0e8e47b
"""
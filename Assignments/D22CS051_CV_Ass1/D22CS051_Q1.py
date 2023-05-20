# -*- coding: utf-8 -*-
"""D22CS051_Q1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QfGp2dN8nh7TEBO7l1hzWn8dL2dV5U9T

# Spot the Difference

## upload image from the folder
"""

from google.colab import files
file = files.upload()

"""## importing the packages"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

"""## spliting the provided image into 2 images"""

# loading image
png_img = cv2.imread("Spot_the_difference.png")
print(f"png image shape: {png_img.shape}")
gray_img = cv2.cvtColor(png_img,cv2.COLOR_BGR2RGB)

# spliting the image
img_1 = gray_img[:,:700//2]
img_2 = gray_img[:,700//2:]

# visulization of the original and seperated images
plt.figure(figsize=(10,9))
plt.title("Original Image")
plt.imshow(png_img[:,:,::-1])
plt.axis(False)
plt.show()
print()
plt.figure(figsize=(10,9))
plt.subplot(1,2,1)
plt.title("Image 1")
plt.imshow(img_1)
plt.axis(False)
plt.subplot(1,2,2)
plt.title("Image 2")
plt.imshow(img_2)
plt.axis(False)
plt.show()

# visulization of the difference in the images
img_diff = img_1 - img_2
plt.figure(figsize=(10,9))
plt.title("Differences")
plt.imshow(img_diff)
plt.axis(False)
plt.show()

# visulization of the markings on the image 1
plt.figure(figsize=(12,10))
img_marked = img_1 + img_diff
plt.subplot(1,2,1)
plt.title("image 1")
plt.imshow(img_1)
plt.axis(False)
plt.subplot(1,2,2)
plt.title("image 2")
plt.imshow(img_2)
plt.axis(False)
plt.show()
print()
plt.figure(figsize=(12,10))
plt.title("marked Images")
plt.imshow(img_marked)
plt.axis(False)
plt.show()
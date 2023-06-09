# -*- coding: utf-8 -*-
"""CV A2-A Q2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lfMBaF3Z7Ot03FMR-vRgIyCJvCrtxujK

# Implement Hough Transform for line detection from scratch

## Getting Data
"""

!wget https://www.mathdoubts.com/cimgs/line/intersecting.png

"""## Self implementation"""

import numpy as np

def hough_line(image, edge_image):
  # image to be drawn on
  dst = edge_image
  # GRAY to BGR
  dst = cv.cvtColor(dst,cv.COLOR_GRAY2BGR)
  
  # Inits #
  edge_height, edge_width = edge_image.shape[:2]
  edge_height_half, edge_width_half = edge_height / 2, edge_width / 2
  d = np.sqrt(np.square(edge_height) + np.square(edge_width))
  num_rhos,num_thetas=90,90
  t_count=900
  dtheta = 180 / num_thetas
  drho = (2 * d) / num_rhos
  thetas = np.arange(0, 180, step=dtheta)
  rhos = np.arange(-d, d, step=drho)
  cos_thetas = np.cos(np.deg2rad(thetas))
  sin_thetas = np.sin(np.deg2rad(thetas))
  accumulator = np.zeros((len(rhos), len(rhos)))
  # Inits end #

  # accumulator calculation 
  for y in range(edge_height):
    for x in range(edge_width):
      if edge_image[y][x] != 0:
        edge_point = [y - edge_height_half, x - edge_width_half]
        for theta_idx in range(len(thetas)):
          rho = (edge_point[1] * cos_thetas[theta_idx]) + (edge_point[0] * sin_thetas[theta_idx])
          theta = thetas[theta_idx]
          rho_idx = np.argmin(np.abs(rhos - rho))
          accumulator[rho_idx][theta_idx] += 1

  # converting rho, theta to line in (x,y) cords.
  for y in range(accumulator.shape[0]):
    for x in range(accumulator.shape[1]):
      if accumulator[y][x] > t_count:
        rho = rhos[y]
        theta = thetas[x]
        a = np.cos(np.deg2rad(theta))
        b = np.sin(np.deg2rad(theta))
        x0 = (a * rho) + edge_width_half
        y0 = (b * rho) + edge_height_half
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        cv.line(dst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
  plt.imshow(dst,cmap="gray")
  plt.show()
  return accumulator, rhos, thetas

import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread("intersecting.png",0)
img = ~img
blur = cv.GaussianBlur(img, (5, 5), 0)
dst = cv.Canny(blur, 50, 200, None, 3)
cdst = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

plt.imshow(img,cmap="gray")
plt.show()
accumulator, thetas, rhos = hough_line(img,dst)

"""## Open-CV implementation"""

src = cv.imread("intersecting.png",0)
src = ~src
dst = cv.Canny(src, 50, 200, None, 3)
    
# Copy edges to the images that will display the results in BGR
cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
cdstP = np.copy(cdst)

lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)

if lines is not None:
    for i in range(0, len(lines)):
        # print(lines[i])
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        # print(rho)
        # print(theta)
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
plt.imshow(src,cmap="gray")
plt.show()
plt.imshow(cdst,cmap="gray")
plt.show()

"""Refrences:-
1. https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html
2. https://towardsdatascience.com/lines-detection-with-hough-transform-84020b3b1549
3. https://alyssaq.github.io/2014/understanding-hough-transform/
"""
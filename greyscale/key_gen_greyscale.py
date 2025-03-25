import random
import numpy as np
import sys
import cv2

filename = sys.argv[1]
img = cv2.imread('inputs/' + filename)

height = img.shape[0]
width = img.shape[1]

key = np.zeros((height, width, 3), np.uint8)

grey_levels = 4
for i in range(height):
    for j in range(width):
        key[i][j] = random.randint(1,grey_levels)*256/grey_levels - 1

cv2.imwrite('outputs/key.png', key)

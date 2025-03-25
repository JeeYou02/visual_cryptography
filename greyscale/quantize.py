import sys
import cv2
import math

N = 4   #gray levels

#filename = sys.argv[1]
img = cv2.imread('outputs/gray_image.png')

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        img[i][j] = math.ceil(((img[i][j][0]+1)/255.0)*N)*255/4

cv2.imwrite('outputs/quantized_image.png', img)

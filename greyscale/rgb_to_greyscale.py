import sys
import cv2

filename = sys.argv[1]
img = cv2.imread('inputs/' + filename)

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imwrite('outputs/gray_image.png', gray_img)

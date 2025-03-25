import cv2

img = cv2.imread('Logo_UniCT.png')

small_img = cv2.resize(img,(1000,493))

cv2.imwrite('image.jpg', small_img)

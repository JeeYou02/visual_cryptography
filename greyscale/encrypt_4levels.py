import numpy as np
import sys
import cv2

def encrypt(n,m):   #n,m are gray levels in {1,2,3,4}
    if(n == 4):
        return m
    if(m == 4):
        return n
    if(n == m):
        return 4
    if(n == 3):
        return abs(m - 2) + 1
    if(n == 2 and m == 1):
        return 3
    return encrypt(m,n)

#img_path = sys.argv[1]
#key_path = sys.argv[2]
key = cv2.imread('outputs/key.png')
img = cv2.imread('outputs/quantized_image.png')

cypher = np.zeros((key.shape[0], key.shape[1],3), np.uint8)

for i in range(key.shape[0]):
    for j in range(key.shape[1]):
        key_val = key[i][j][0]
        img_val = img[i][j][0]

        cypher[i][j] = encrypt((key_val+1)/64, (img_val+1)/64)*64 - 1

cv2.imwrite('outputs/cypher.png', cypher)

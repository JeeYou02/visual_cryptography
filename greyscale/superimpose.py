import cv2
import numpy as np
import sys

def superimpose(img1, img2):
    assert img1.shape[2] == 4 and img2.shape[2] == 4, "Images must have 4 channels (RGBA)"
    assert img1.shape == img2.shape, "Images must have the same dimensions"

    output_img = np.zeros_like(img1)

    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            if img1[i][j][3] == 255 and img2[i][j][3] == 255:
                output_img[i][j][3] = 255
            elif img1[i][j][3] == 0 and img2[i][j][3] == 0:
                output_img[i][j] = [255, 255, 255, 255]
            else:
                output_img[i][j][3] = img1[i][j][3] + img2[i][j][3]
    
    return output_img

filename1 = sys.argv[1]
filename2 = sys.argv[2]
img1 = cv2.imread('outputs/' + filename1, cv2.IMREAD_UNCHANGED)
img2 = cv2.imread('outputs/' + filename2, cv2.IMREAD_UNCHANGED)

cv2.imwrite('outputs/superimposed_output.png', superimpose(img1, img2))

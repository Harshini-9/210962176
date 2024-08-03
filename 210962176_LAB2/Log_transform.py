# log transformation
import cv2
import numpy as np

# load image
img = cv2.imread("logtest.jpg")

# Apply log transformation
img_log = (np.log(img+1)/(np.log(1+np.max(img))))*255

# Specify the data type
img_log = np.array(img_log,dtype=np.uint8)

# Display the image
cv2.imshow('log_image',img_log )
cv2.waitKey(0)
# Image negative

# import cv2 module
import cv2

# Load the image
img = cv2.imread('zoo.jpg')

# Invert the image using cv2.bitwise_not
img_neg = cv2.bitwise_not(img)

# Show the image
cv2.imshow('negative', img_neg)

# Use wait key to display
cv2.waitKey(0)
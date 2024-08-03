# Gray level slicing
import cv2

# load the input image
img = cv2.imread("zoo.jpg")

# use of cvtColor() function to grayscale the image
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow('GrayScale', gray_image)

cv2.waitKey(0)

cv2.destroyAllWindows()
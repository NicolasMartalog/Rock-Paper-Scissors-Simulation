import cv2

image=cv2.imread("real.gif")

scale_percent=2.0

width=int(image.shape[1]*scale_percent)

height=int(image.shape[0]*scale_percent)

dimension=(width,height)

resized = cv2.resize(image,dimension, interpolation = cv2.INTER_AREA)

print(resized.shape)

cv2.imwrite("output.gif",resized)
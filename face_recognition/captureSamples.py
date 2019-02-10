import numpy as np
import cv2
import time

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(3,480)

count = 0
while count < 5:
	ret, img = cam.read()
	cv2.imwrite(str(count) + ".jpg", img)
	k = cv2.waitKey(300) & 0xff # Press 'ESC' for exiting video
	count +=1 
cam.release()
cv2.destroyAllWindows()
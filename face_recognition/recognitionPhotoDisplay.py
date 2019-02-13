import cv2
import numpy as np
import time
import os 

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "Cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['Maciek','Patryk', 'Wojtek', 'Dawid'] 

# cam = cv2.VideoCapture(0)
# cam.set(3, 640) # set video widht
# cam.set(4, 480) # set video height

img = cv2.imread('1.jpg',0) 

minW = 0.1* 640 #cam.get(3)
minH = 0.1* 480 #cam.get(4)



#ret, img =cam.read()
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale( 
    img,
    scaleFactor = 1.1,
    minNeighbors = 4,
    minSize = (int(minW), int(minH)),
   )

for(x,y,w,h) in faces:

    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

    id, confidence = recognizer.predict(img[y:y+h,x:x+w])
    #print("int" + str(confidence))
    if (confidence < 80 and confidence > 0):
        id = names[id]
        print(id)            
        confidence = "  {0}%".format(round(100 - confidence))
     #   print("str" + confidence)

    else:
        id = "unknown"
        confidence = "  {0}%".format(round(100 - confidence))
    
    cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
    cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  

cv2.imshow('camera',img) 

    # k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    # if k == 27:
    #     break
cv2.waitKey(0)

print("\n [INFO] Exiting Program and cleanup stuff")
#cam.release()
cv2.destroyAllWindows()
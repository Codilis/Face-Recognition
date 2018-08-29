import cv2
import os
import glob
from database import Connection

##===================Connection Establishment=====================================================================
username, password = 'username', 'password'
conn = Connection(username, password)
conn.connect()
conn.create_table()

name=input('Enter your name ')
x = conn.insert_value(name)

ids = conn.select_value(name)
conn.close_connection()
##=====================Camera Starts for dataset creation==========================================================

cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('cascade/haarcascade_frontalface_default.xml')
if(int(x) == 1):
    q = "dataset/"+str(ids)+"*.jpg"
    w = []
    for file in glob.glob(q):
        w.append(int(file.strip().split('\\')[-1].split('.')[1]))
    i = sorted(w)[-1]
    print("i =",i) 
else:
    i=0
offset=50
os.makedirs('dataset', exist_ok=True)
j = i+21
print("j =",j)
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    for(x,y,w,h) in faces:
        i=i+1
        cv2.imwrite("dataSet/"+str(ids) +'.'+ str(i) + ".jpg", gray[y-offset:y+h+offset,x-offset:x+w+offset])
        cv2.rectangle(im,(x-50,y-50),(x+w+100,y+h+100),(225,0,0),2)
        cv2.imshow('im',im[y-offset:y+h+offset,x-offset:x+w+offset])
        cv2.waitKey(100)
    if i>j:
        cam.release()
        cv2.destroyAllWindows()
        break

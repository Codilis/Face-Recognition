import cv2
from database import Connection

username, password = 'username', 'password'
conn = Connection(username, password)
conn.connect()
data = conn.select_all()
names_dict = {}
for ids, name in data:
    names_dict[str(ids)] = name
conn.close_connection()

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read('trainer/trainer.yml')
cascadePath = "cascade/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
path = 'dataSet'

cam = cv2.VideoCapture(0)

fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 255, 255)
##width_d, height_d = 720, 720

while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    for(x,y,w,h) in faces:
##        nbr_predicted, conf = recognizer.predict(cv2.resize(gray[y:y+h,x:x+w], (width_d, height_d)))
        nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
        cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        #print(names_dict[str(nbr_predicted)], str(nbr_predicted)+"--"+str(conf))
        cv2.putText(im,names_dict[str(nbr_predicted)],
                    (x,y+h),fontFace , fontScale , fontColor) #Draw the text
    cv2.imshow('im',im)
    cv2.waitKey(10)

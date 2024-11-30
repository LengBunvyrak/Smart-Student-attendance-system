import cv2
import numpy as np
import face_recognition as fr
import os
from datetime import datetime

def resize(img, size):
    width = int(img.shape[1]*size)
    height = int(img.shape[0]*size)
    dimension = (width, height)
    return cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)

path = 'final project\student_faces'
studentImg = []
studentName = []

myList = os.listdir(path)


for cl in myList:
    currentImg = cv2.imread(f'{path}\{cl}')
    studentImg.append(currentImg)
    studentName.append(os.path.splitext(cl)[0]) # split the .jpg


def findEncoding(images):
    encodingList = []
    for image in images:
        image = resize(image, 0.50)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encodeimage = fr.face_encodings(image)[0]
        encodingList.append(encodeimage)

    return encodingList

def Attendace(name):
    with open(r'final project\attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        # for loop for the name of students that had been written down
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.now()
            timestr = now.strftime('%H: %M')
            formatted_date = now.strftime('%Y-%m-%d')
            f.writelines(f'\n{name}, {timestr}, {formatted_date}')

encodeList = findEncoding(studentImg)

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Check if the computer is using GPU acceleration for smoother video capture
if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    print("Using GPU for acceleration.")
else:
    print("No GPU detected, using CPU.")

while True:
    success, frame = video.read()

    frames = cv2.resize(frame, (0,0), None, 0.25, 0.25) # small frame
    frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)

    # recognize multiple frame at the same time
    # detect faces and encode
    faceinFrame = fr.face_locations(frames, model='cnn') # the model is gpu acceleration
    encodeFacesinFrame = fr.face_encodings(frames, faceinFrame)

    for encodeFace, faceLocation in zip(encodeFacesinFrame, faceinFrame): # we can compare faces one by one
        # compare the face in the frame with the sample
        matches = fr.compare_faces(encodeList, encodeFace)
        faceDistance = fr.face_distance(encodeList, encodeFace)
        print(faceDistance)
        matchIndex = np.argmin(faceDistance)
        
        # if condition to see if the face is match up

        if matches[matchIndex]:
            #if it matches we draw a rectangle around the face
            name = studentName[matchIndex].upper()
            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4  # to expand the small frame to full frame
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 3)
            cv2.rectangle(frame, (x1, y2-25), (x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(frame, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1 ,(255,255,255), 2)
            Attendace(name)

        cv2.imshow('video',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()

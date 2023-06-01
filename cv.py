import cv2
import datetime
import time
import pyautogui

absolut_X = 1920
absolut_Y = 1080
num_faces = 5
scale_picture_on_screen = 0.5
speed = 50

saved_faces = []
offsets = {'X': 0, 'Y': 0}
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )
    if len(faces):
        saved_faces.append(faces[0])
        if saved_faces.__len__() > 5:
            saved_faces.pop(0)
        
        num = saved_faces.__len__()
        x, y, w, h = 0, 0, 0, 0
        for face in saved_faces:
            x += face[0] / num
            y += face[1] / num
            w += face[2] / num
            h += face[3] / num
        x, y, w, h = [int(i) for i in [x,y,w,h]]
        
        height, width, channels = frame.shape

        relX = x / (width - w)
        relY = y / (height - h)
        
        for [relPos, offset] in ([1-relX, 'X'], [relY, 'Y']):
            if relPos < 0.25 or relPos > 0.75:
                offsets[offset] += (-0.5 + relPos) * speed            

        relX *= scale_picture_on_screen
        relY *= scale_picture_on_screen

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        pyautogui.moveTo(absolut_X * 2 - relX * absolut_X + offsets['X'], relY * absolut_Y + offsets['Y'])


    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

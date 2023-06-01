import cv2
import datetime
import time
import pyautogui

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
        x, y, w, h = faces[0]
        height, width, channels = frame.shape

        relX = x / (width - w)
        relY = y / (height - h)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        pyautogui.moveTo(1920 * 2 - relX * 1920, relY * 1080)


    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

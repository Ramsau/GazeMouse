from enum import Enum
import cv2
import datetime
import time
import pyautogui
from gaze_tracking import GazeTracking
import socket

class Direction(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    
absolut_X = 1920
absolut_Y = 1080
num_faces = 5
scale_picture_on_screen = 0.5
speed = 50
tracking = Direction.HORIZONTAL

saved_faces = []
offsets = {'X': 0, 'Y': 0}
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

gaze = GazeTracking()
video_capture = cv2.VideoCapture(0)
cv2.namedWindow('custom_win', cv2.WINDOW_FREERATIO)


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
counter = 0



while True:
    ret, frame = video_capture.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)#

    frame = gaze.annotated_frame()#
    text = ""
    relative_shift = 0
    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        relative_shift = speed
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
        relative_shift = -speed
    elif gaze.is_center():
        text = "Looking center"
    
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    try: print(text + '\t\t' + str(gaze.eye_left.pupil.x) + '\t\t' + str(gaze.eye_left.pupil.y))
    except: pass
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


    if tracking == Direction.HORIZONTAL:
        absolut_X += relative_shift
    elif tracking == Direction.VERTICAL:
        absolut_Y += relative_shift
    pyautogui.moveTo(absolut_X, absolut_Y)
    
    counter += 1
    if counter % 50 == 0:
        s.send(b"Request")
        data = s.recv(BUFFER_SIZE)
        if data == b'Horizontal':
            tracking = Direction.HORIZONTAL
        elif data == b'Vertical':
            tracking = Direction.VERTICAL
        print ("\n#####################\nreceived data:" +str(data) + "\n#######################" )

    try: cv2.imshow('Video', frame) 
    except: pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
s.close()

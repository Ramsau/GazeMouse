import cv2
import serial
import datetime
import time

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
multiplicatorX = 0.075
multiplicatorY = -0.075
servoConst = 0.2
servoSpeed = 0.005
serX = 90
serY = 90
maxY = 117
minY = 55
waitTime = datetime.timedelta(seconds=3)
marginForShoot = 25

lastFound = datetime.datetime.now()
lastLost = datetime.datetime.now()
shoot = 0
video_capture = cv2.VideoCapture(0)
serl = serial.Serial('/dev/ttyUSB0')
lastdx = 0
lastdy = 0


def writeSerial(x, y, shoot):
    string = "{}-{},{}".format(
        int(x), int(y), int(shoot)
    )
    serl.write(str.encode(string))


while True:
    now = datetime.datetime.now()
    timeSinceLast = now - lastFound
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )
    if len(faces) and timeSinceLast.total_seconds() > servoConst + abs(max(lastdx, lastdy) * servoSpeed):
        lastFound = now

        x, y, w, h = faces[0]
        height, width, channels = frame.shape

        dx = width / 2 - x - w / 2
        dy = height / 2 - y - h / 2
        lastdx = dx
        lastdy = dy

        serX += dx * multiplicatorX
        serY += dy * multiplicatorY
        serY = min(maxY, serY)
        serY = max(minY, serY)

        if(max(dx, dy) < marginForShoot):
            shoot = 1
        else:
            shoot = 0

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print(max(dx, dy) * servoSpeed)


        writeSerial(serX, serY, shoot)

    if not len(faces):
        lastLost = datetime.datetime.now()

    if(timeSinceLast > waitTime):
        print("go back")
        writeSerial(90, 90, 0)

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
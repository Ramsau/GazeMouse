import speech_recognition
import pyttsx3
import sys
import mouse
import socket

left_click = ["left click", "left kick", "left kit", "lift kit", "netflix"]
right_click = ["right click", "right kick", "right kit", "right quick"]
middle_click = ["middle click", "middle creek"]
select = ["select"]
exit = ["terminate", "close program", "exit"]

recognizer = speech_recognition.Recognizer()

lock = False


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print ('Connection address:' + str(addr))

    

while True:

    data = conn.recv(BUFFER_SIZE)
    print ("received data:" + str(data))
    conn.send(b"Vertical")  # Vertical or Horizontal or Nothing to be returned here
    print ("sended infromation")

    try:

        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio)
            text = text.lower()
            if lock is False:

                print(f"Recognized {text}")
                if text in left_click:
                    mouse.click('left')
                    print(f"Execute left_click")
                elif text in right_click:
                    mouse.click('right')
                    print(f"Execute right_click")
                elif text in middle_click:
                    mouse.click('middle')
                    print(f"Execute middle_click")
                elif text in select:
                    mouse.hold('left')
                    print(f"Execute middle_click")
                elif text == "stop":
                    mouse.release('left')
                    mouse.release('middle')
                    print(f"Execute middle_click")
                elif text == "scroll":
                    mouse.hold('middle')
                elif text in exit:
                    print(f"Execute exit")
                    sys.exit(0)
                elif text == "mute":
                    print(f"Execute mute")
                    lock = True

            if text == "unmute":
                print(f"Execute unmute")
                lock = False


    except speech_recognition.UnknownValueError:

        recognizer = speech_recognition.Recognizer()
        continue
    


    
conn.close()
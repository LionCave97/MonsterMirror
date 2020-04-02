import multiprocessing
import RPi.GPIO as GPIO
from shutil import rmtree
from os import mkdir
import numpy as np
import picamera
import face_recognition
from time import sleep
print("MonsterMirror")

print("Starting up")
print("Importing")


print("Done importing")
print("Setup")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

touchSwitch = 18
outputPin = 15
buzzerPin = 14
startup = True

r1 = 2
g1 = 3
b1 = 4

r2 = 17
g2 = 27
b2 = 22

r3 = 10
g3 = 9
b3 = 11

r4 = 21
g4 = 20
b4 = 16

r5 = 13
g5 = 19
b5 = 26

GPIO.setup(touchSwitch, GPIO.IN)
GPIO.setup(outputPin, GPIO.OUT)
GPIO.output(outputPin, False)
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, False)

GPIO.setup(r1, GPIO.OUT)
GPIO.setup(g1, GPIO.OUT)
GPIO.setup(b1, GPIO.OUT)

GPIO.setup(r2, GPIO.OUT)
GPIO.setup(g2, GPIO.OUT)
GPIO.setup(b2, GPIO.OUT)

GPIO.setup(r3, GPIO.OUT)
GPIO.setup(g3, GPIO.OUT)
GPIO.setup(b3, GPIO.OUT)

GPIO.setup(r4, GPIO.OUT)
GPIO.setup(g4, GPIO.OUT)
GPIO.setup(b4, GPIO.OUT)

GPIO.setup(r5, GPIO.OUT)
GPIO.setup(g5, GPIO.OUT)
GPIO.setup(b5, GPIO.OUT)


GPIO.output(r1, False)
GPIO.output(g1, False)
GPIO.output(b1, False)

GPIO.output(r2, False)
GPIO.output(g2, False)
GPIO.output(b2, False)

GPIO.output(r3, False)
GPIO.output(g3, False)
GPIO.output(b3, False)

GPIO.output(r4, False)
GPIO.output(g4, False)
GPIO.output(b4, False)

GPIO.output(r5, False)
GPIO.output(g5, False)
GPIO.output(b5, False)

print("Setup Done")
rmtree("pics", ignore_errors=True)
mkdir("pics")
print("Pics Folder cleared")

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
print("Starting Camera")
camera = picamera.PiCamera()
camera.resolution = (96, 96)
# camera.resolution = (320, 240)
output = np.empty((96, 96, 3), dtype=np.uint8)

print("Camera Started")


# Initialize some variables
face_locations = []
pics = 0
counter = 0
touch = False

def StartUpF():
    GPIO.output(r1, True)
    GPIO.output(g1, True)
    GPIO.output(b1, True)

    GPIO.output(r2, True)
    GPIO.output(g2, True)
    GPIO.output(b2, True)

    GPIO.output(r3, True)
    GPIO.output(g3, True)
    GPIO.output(b3, True)

    GPIO.output(r4, True)
    GPIO.output(g4, True)
    GPIO.output(b4, True)

    GPIO.output(r5, True)
    GPIO.output(g5, True)
    GPIO.output(b5, True)
    GPIO.output(buzzerPin, True)
    sleep(1)
    GPIO.output(buzzerPin, False)
    GPIO.output(r1, False)
    GPIO.output(g1, False)
    GPIO.output(b1, False)

    GPIO.output(r2, False)
    GPIO.output(g2, False)
    GPIO.output(b2, False)

    GPIO.output(r3, False)
    GPIO.output(g3, False)
    GPIO.output(b3, False)

    GPIO.output(r4, False)
    GPIO.output(g4, False)
    GPIO.output(b4, False)

    GPIO.output(r5, False)
    GPIO.output(g5, False)
    GPIO.output(b5, False)

def ledOff():
    GPIO.output(r1, False)
    GPIO.output(g1, False)
    GPIO.output(b1, False)

    GPIO.output(r2, False)
    GPIO.output(g2, False)
    GPIO.output(b2, False)

    GPIO.output(r3, False)
    GPIO.output(g3, False)
    GPIO.output(b3, False)

    GPIO.output(r4, False)
    GPIO.output(g4, False)
    GPIO.output(b4, False)

    GPIO.output(r5, False)
    GPIO.output(g5, False)
    GPIO.output(b5, False)

def breath():
    if not touch:
        global counter
        if counter == 1:
            GPIO.output(b1, False)
            GPIO.output(b5, False)
            GPIO.output(r1, True)
            GPIO.output(r5, True)
        if counter == 2:
            GPIO.output(b2, False)
            GPIO.output(b4, False)
            GPIO.output(r2, True)
            GPIO.output(r4, True)
        if counter == 3:
            GPIO.output(b3, False)
            GPIO.output(r3, True)
        if counter == 4:
            GPIO.output(r1, False)
            GPIO.output(r5, False)
            GPIO.output(g1, True)
            GPIO.output(g5, True)
        if counter == 5:
            GPIO.output(r2, False)
            GPIO.output(r4, False)
            GPIO.output(g2, True)
            GPIO.output(g4, True)
        if counter == 6:
            GPIO.output(r3, False)
            GPIO.output(g3, True)
        if counter == 7:
            GPIO.output(g1, False)
            GPIO.output(g5, False)
            GPIO.output(b1, True)
            GPIO.output(b5, True)
        if counter == 8:
            GPIO.output(g2, False)
            GPIO.output(g4, False)
            GPIO.output(b2, True)
            GPIO.output(b4, True)
        if counter == 9:
            GPIO.output(g3, False)
            GPIO.output(b3, True)
            counter = 0
            
    counter = counter + 1
    sleep(1)


def touched():
    switchTouched = GPIO.input(touchSwitch)
    global touch
    if switchTouched:
        touch = True
        ledOff()
    else:
        touch = False
        print("not touched")
    print(touch)

def capture():
    global touch

    if touch:
        global counter
        counter = 0
        GPIO.output(buzzerPin, True)
        sleep(0.10)
        GPIO.output(buzzerPin, False)
        ledOff()
        print("touch detected")
        print("Capturing image.")
        global face_locations
        # Grab a single frame of video from the RPi camera as a numpy array
        camera.capture(output, format="rgb")
        print("Captured finding faces")

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(output)
        print("Found {} faces in image.".format(len(face_locations)))

        if len(face_locations) > 0:

            GPIO.output(r1, True)
            GPIO.output(buzzerPin, True)
            sleep(0.30)
            GPIO.output(r2, True)
            GPIO.output(buzzerPin, False)
            sleep(0.30)
            GPIO.output(r3, True)
            GPIO.output(buzzerPin, False)
            sleep(0.30)
            GPIO.output(r4, True)
            GPIO.output(buzzerPin, False)
            sleep(0.30)
            GPIO.output(r5, True)
            GPIO.output(buzzerPin, False)
            sleep(0.30)

            GPIO.output(b1, True)
            GPIO.output(buzzerPin, True)
            sleep(0.15)
            GPIO.output(b2, True)
            GPIO.output(buzzerPin, False)
            sleep(0.15)
            GPIO.output(b3, True)
            GPIO.output(buzzerPin, False)
            sleep(0.15)
            GPIO.output(b4, True)
            GPIO.output(buzzerPin, False)
            sleep(0.15)
            GPIO.output(b5, True)
            GPIO.output(buzzerPin, False)
            sleep(0.15)

            GPIO.output(g1, True)
            GPIO.output(buzzerPin, True)
            sleep(0.15)
            GPIO.output(g2, True)
            GPIO.output(buzzerPin, False)
            sleep(0.15)
            GPIO.output(g3, True)
            GPIO.output(buzzerPin, False)
            sleep(0.15)
            GPIO.output(g4, True)
            GPIO.output(buzzerPin, False)
            sleep(0.15)
            GPIO.output(g5, True)
            GPIO.output(buzzerPin, False)
            sleep(0.15)

            GPIO.output(buzzerPin, True)
            global pics            
            pics = pics + 1
            print("taking pic")
            camera.resolution = (3280, 2464)
            camera.capture('pics/image' + str(pics) + '.jpg')
            print("captured")
            camera.resolution = (96, 96)
            GPIO.output(buzzerPin, False)
            ledOff()
            sleep(1)

            GPIO.output(r5, True)
            sleep(0.15)
            GPIO.output(r4, True)
            sleep(0.15)
            GPIO.output(r3, True)
            sleep(0.15)
            GPIO.output(r2, True)
            sleep(0.15)
            GPIO.output(r1, True)
            sleep(0.25)

            GPIO.output(r5, False)
            sleep(0.10)
            GPIO.output(r4, False)
            sleep(0.10)
            GPIO.output(r3, False)
            sleep(0.10)
            GPIO.output(r2, False)
            sleep(0.10)
            GPIO.output(r1, False)
            sleep(0.10)

            GPIO.output(g5, True)
            sleep(0.15)
            GPIO.output(g4, True)
            sleep(0.15)
            GPIO.output(g3, True)
            sleep(0.15)
            GPIO.output(g2, True)
            sleep(0.15)
            GPIO.output(g1, True)
            sleep(0.25)

            GPIO.output(g5, False)
            sleep(0.10)
            GPIO.output(g4, False)
            sleep(0.10)
            GPIO.output(g3, False)
            sleep(0.10)
            GPIO.output(g2, False)
            sleep(0.10)
            GPIO.output(g1, False)
            sleep(0.10)

            GPIO.output(b5, True)
            sleep(0.15)
            GPIO.output(b4, True)
            sleep(0.15)
            GPIO.output(b3, True)
            sleep(0.15)
            GPIO.output(b2, True)
            sleep(0.15)
            GPIO.output(b1, True)
            sleep(0.25)

            GPIO.output(b5, False)
            sleep(0.10)
            GPIO.output(b4, False)
            sleep(0.10)
            GPIO.output(b3, False)
            sleep(0.10)
            GPIO.output(b2, False)
            sleep(0.10)
            GPIO.output(b1, False)
            sleep(0.10)


try:
    while True:
       
        if startup:
           StartUpF()
           startup= False
       
        p1 = multiprocessing.Process(touched())    
        p2 = multiprocessing.Process(breath())
        p3 = multiprocessing.Process(capture())

        p1.start()
        p2.start()
        p3.start()


    sleep(0.30)

except:
    GPIO.cleanup()
    print("MonsterMirror Stopped")
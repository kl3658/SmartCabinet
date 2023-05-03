from global_ import camera
from fractions import Fraction
#from tmlib import *
from mfrc522 import SimpleMFRC522
import random
import math
import spidev
import time
import picamera.array
import time
import sys
#import cv2
import RPi.GPIO as GPIO
import numpy as np
"""
def info():
    #Prints a basic library description
    print('Software library for the SmartCabinet project.')

def cameraSetup():

    #This is used to st up the properties of the PiCamera
    #Settings can be changed through editing the fucntions themselves
    camera.resolution = (640, 480)
    camera.framerate = 24
    camera.iso = 400
    camera.vflip = True             # Camera is upside down, so get it rightside-up
    time.sleep(2)
    print("Camera set up successfully!")

    # Load the model - one time only during startup
    tm = TeachableMachineTf()
    tm.load('/home/pi/teachablemachine-python/tflite_model/model_unquant.tflite', '/home/pi/teachablemachine-python/tflite_model/labels.txt')

def turnOnCamera():
    '''
    Turn on the camera by having us look at the preview on the main screen. May not work with VNC
    '''
    camera.start_preview()
    time.sleep(2)
    print("Camera turned on!")

def savePhotoToFile(img_counter, nightModeVal):
    '''
    Simply saves an image to somewhere on the Raspberry Pi. The directory can be altered.
    '''
    img_name = "/home/pi/Pictures/image{}.jpg".format(img_counter)
    # Allow some time to take an image. If night mode is set, this should take 30 seconds
    if nightModeVal == 1:
        time.sleep(30)
    else:
        time.sleep(2)
    camera.capture(img_name)
    print("{} written!".format(img_name))

def predict_face():
    # Each time you want to capture an image - Turn on camera
    cap = cv2.VideoCapture(0)
    # Get image
    _, img = cap.read()

    # Pass image to model, get ID of most likely person
    res, name = tm.predict(img)
    idx = np.argmax(res)
    print("Name: ", name)
    print("Res: ", res)
    print("idx: ", idx)

def captureYUVArray(array_counter, nightModeVal):
    '''
    Similar to savePhotoToFile, except it captures a YUV image and array instead.
    '''
    with picamera.array.PiYUVArray(camera) as output:
        array_name = "/home/pi/Pictures/YUVarray{}.jpg".format(array_counter)
        # Allow some time to take an image. If night mode is set, this should take 30 seconds
        if nightModeVal == 1:
            time.sleep(30)
        else:
            time.sleep(2)
        camera.capture(array_name, 'yuv')
        print("{} written!".format(output))
        # Show size of YUV data
        print('Array Shape: ', output.array.shape)
        # Show size of RGB converted data
        print('RGB Array Shape: ', output.rgb_array.shape)

def flipVerticalOrient():
    camera.vflip = not camera.vflip

def setISOofCamera():
    while True:
        try:
            isovalue = int(input('Enter an ISO value between 0 and 1600. 0 will set it to AUTO:'))
            if (isovalue < 0) or (isovalue > 1600):
                raise ValueError
            camera.iso = isovalue
            break
        except ValueError:
            print('Integers only please! If you did enter an integer, it was an illegal value!')
            continue

def setFramerateofCamera():
    while True:
        try:
            framerateVal = int(input('Enter an framerate value:'))
            if (framerateVal < 0) or (framerateVal > 60):
                raise ValueError
            camera.framerate = framerateVal
            break
        except ValueError:
            print('Integers only please! If you did enter an integer, it was an illegal value!')
            continue

def nightModeSet(nightModeVal):
    '''
    Asks to set night mode or not. Predetermined settings for night mode shown below.

    Adapted from:
    https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-in-low-light
    '''
    while True:
        try:
            nightModeVal = int(input("Would you like to set night mode? 0 for NO, 1 for YES: "))
            if (nightModeVal != 0) and (nightModeVal != 1):
                raise ValueError
            elif (nightModeVal == 1):
                camera.framerate = Fraction(1, 6)
                camera.shutter_speed = 6000000      # This is in microseconds, so this is 6 seconds
                camera.iso = 800
            elif (nightModeVal == 0):
                camera.framerate = 30
                camera.shutter_speed = 0            # Automatic at 0
                camera.iso = 800
            return nightModeVal
        except ValueError:
            print('Integers only please! If you did enter an integer, it was an illegal value!')
            continue

def useCamera():
    '''
    While the camera is turned on, we can perform various properties, such as taking pictures and even
    being to change its properties on the fly.
    '''
    img_val = 1
    nightModeBit = 0
    time.sleep(2)
    while True:
        key = input('Press key, then hit Enter. Enter p to snap a photo. Enter q to exit: ')
        if key == 'f':
            print('Flipping Vertical Orientation...')
            flipVerticalOrient()
        if key == 'i':
            print('Changing ISO of the Camera...')
            setISOofCamera()
        if key == 'p':
            print('Taking Picture...')
            savePhotoToFile(img_val, nightModeBit)
            print('Predicting...')
            predict_face()
            print('Taking YUV array...')
            captureYUVArray(img_val, nightModeBit)
            img_val += 1
        if key == 'n':
            print('Night Mode Activate...')
            nightModeBit = nightModeSet(nightModeBit)
        if key == 'r':
            print('Setting framerate...')
            setFramerateofCamera()
        if key == 'q':
            print('Quitting Camera...')
            camera.stop_preview()
            break
"""

''' Task 1 '''
# Keypad part goes here. Remember to somehow get them into functions and even have properties
# called via functions like with the picamera stuff. Also a password system. GPIO Pins are shown for the keypad

R1 = 12
R2 = 16
R3 = 20
R4 = 21

C1 = 13
C2 = 19
C3 = 26

# Initialize the GPIO pins

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# The readLine function implements the procedure discussed in the article
# It sends out a single pulse to one of the rows of the keypad
# and then checks each column for changes
# If it detects a change, the user pressed the button that connects the given line
# to the detected column

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        print(characters[0])
    if(GPIO.input(C2) == 1):
        print(characters[1])
    if(GPIO.input(C3) == 1):
        print(characters[2])
    GPIO.output(line, GPIO.LOW)

try:
    while True:
        # call the readLine function for each row of the keypad
        readLine(R1, ["1","2","3"])
        readLine(R2, ["4","5","6"])
        readLine(R3, ["7","8","9"])
        readLine(R4, ["*","0","#"])
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nApplication stopped!")

''' Task 2 '''
# Servo part starts here

servoPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)      # GPIO 18 for PWM with 50Hz
p.start(2.5)                    # Initialization

try:
    while True:
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(2.5)
        time.sleep(0.5)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()

''' Task 3 '''
# RFID Part Code Starts Here

reader = SimpleMFRC522()

print("Hold a tag near the reader")
print("Reading tag in 1 second...")
time.sleep(1)

# Keep it for now. We only want it to run if the user calls for it from the browser UI.
id = reader.read_id_no_block()

if id:
    print(hex(id))
else:
    print("No tag detected")

GPIO.cleanup()

''' Task 4 '''
# Section for the Load Cell Code

EMULATE_HX711=False

referenceUnit = 1       # Reference Value of Tommy's Phone

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()

hx = HX711(5, 6) #GPIO Pins 5 and 6

hx.set_reading_format("LSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.

        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string

        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = hx.get_weight(5)
        print(val)

        # To get weight from both channels (if you have load cells hooked up
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


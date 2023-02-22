import random
import math
import spidev
import time
import RPi.GPIO as GPIO
import picamera
import picamera.array
# import cv2

def info():
    '''Prints a basic library description'''
    print('Software library for the SmartCabinet project.')

def cameraSetup():
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 24
    time.sleep(5)
    print("Camera set up successfully!")
    return True

def turnOnCamera():
    camera = picamera.PiCamera()
    camera.start_preview()
    time.sleep(5)
    camera.stop_preview()
    print("Camera turned on!")

def takePictureOfFace():
    '''
    TODO: Pass an image counter, the name of the image itself, and someImage
    '''
    img_name = "images/" + name + "/image{}.jpg".format(img_name)
    cv2.imwrite(img_name, someImage)
    print("{} written!".format(img_name))
    # img_counter += 1
    
def identifyFace():
    '''
    This will open up a video feed that is played through cv2
    The first two lines will simply make sure that the camera is continuously rolling
    while we play around with it and have it detect faces for us
    '''
    camera = picamera.PiCamera()
    rawCapture = picamera.array.PiRGBArray(camera, size=(640, 480))
    time.sleep(2)
    while True:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            someImage = frame.array

            # show the frame
            cv2.imshow("Press Space to take an image, ESC to exit", someImage)
            key_press = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

            # If ESC key pressed, we break out of this loop to stop the program
            # If we hit SPACE, we take an image by taking a photo
            if key_press == 27:
                break
            elif key_press == 32:
                takePictureOfFace()

# Define Variables
delay = 0.5
pad_channel = 0

# Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000

def readadc(adcnum):
   # read SPI data
   if adcnum > 7 or adcnum < 0:
       return -1
   r = spi.xfer2([1, 8 + adcnum << 4, 0])
   data = ((r[1] & 3) << 8) + r[2]
   return data

try:
   while True:
       pad_value = readadc(pad_channel) + 1
       new_pad_value = pad_value * math.log(pad_value) * 16.5
       new_pad_lbs = new_pad_value * .0022
       print("---------------------------------------")
       print("Pressure Pad Value: %d" % new_pad_value + "g or: " + str(new_pad_lbs) + "lbs")
       time.sleep(delay)
except KeyboardInterrupt:
   pass

import random
import spidev
import time
import RPi.GPIO as GPIO
import picamera
import cv2

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
    
def identifyFace():
    '''The faceIdentified is a placeholder for when we implement a system to detect faces'''
    print("This is the person taking candy from the container!")
    faceIdentified = bool(random.choice([True, False]))
    return faceIdentified
    
def takePictureOfFace():
    faceThere = identifyFace()
    if faceThere == True:
        print("Photo taken!")
    else:
        print("No photo taken...")


# Define Variables
# delay = 0.5
# pad_channel = 0

# Create SPI
# spi = spidev.SpiDev()
# spi.open(0, 0)
# spi.max_speed_hz=1000000

# def readadc(adcnum):
#    # read SPI data
#    if adcnum > 7 or adcnum < 0:
#        return -1
#    r = spi.xfer2([1, 8 + adcnum << 4, 0])
#    data = ((r[1] & 3) << 8) + r[2]
#   return data

# try:
#    while True:
#        pad_value = readadc(pad_channel)
#        print("---------------------------------------")
#        print("Pressure Pad Value: %d" % pad_value)
#        time.sleep(delay)
# except KeyboardInterrupt:
#    pass

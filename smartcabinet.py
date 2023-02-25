import random
import math
import spidev
import time
import RPi.GPIO as GPIO
#import picamera                     # Implemented in global_ file
import picamera.array
from global_ import camera
from fractions import Fraction
#import cv2                          # Will be discussed later on

# Create PiCamera and global variables
#camera = picamera.PiCamera()

def info():
    '''Prints a basic library description'''
    print('Software library for the SmartCabinet project.')

def cameraSetup():
    '''
    This is used to st up the properties of the PiCamera
    Settings can be changed through editing the fucntions themselves
    '''
    camera.resolution = (640, 480)
    camera.framerate = 24
    camera.iso = 400
    camera.vflip = True             # Camera is upside down, so get it rightside-up
    time.sleep(2)
    print("Camera set up successfully!")

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
        camera.capture(output, 'yuv')
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
                camera.sensor = 3
                camera.shutter_speed = 6000000      # This is in microseconds, so this is 6 seconds
                camera.iso = 800
            elif (nightModeVal == 0):
                camera.framerate = 30
                camera.sensor = 0
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

# Define Variables
delay = 0.5
pad_channel = 0

# Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000

def readadc(adcnum):
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
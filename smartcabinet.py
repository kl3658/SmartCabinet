import random
import math
import spidev
import time
import RPi.GPIO as GPIO
#import picamera                     # Implemented in global_ file
import picamera.array
from global_ import camera
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

def savePhotoToFile(img_counter):
    '''
    Simply saves an image to somewhere on the Raspberry Pi. The directory can be altered.
    '''
    img_name = "/home/pi/Pictures/image{}.jpg".format(img_counter)
    # Allow some time to take an image
    time.sleep(2)
    camera.capture(img_name)
    print("{} written!".format(img_name))

def captureYUVArray(array_counter):
    '''
    Similar to savePhotoToFile, except it captures a YUV image and array instead.
    '''
    with picamera.array.PiYUVArray(camera) as output:
        array_name = "/home/pi/Pictures/YUVarray{}.jpg".format(array_counter)
        # Allow some time to take an image
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
            break
        except ValueError:
            print('Integers only please! If you did enter an integer, it was an illegal value!')
            continue
    
def useCamera():
    '''
    While the camera is turned on, we can perform various properties, such as taking pictures and even
    being to change its properties on the fly.
    TODO: Rewrite the function to do basic stuff. OPTIONAL: Find ways to implement more functions to
    change while this program is running, mainly through keybindings.
    '''
    img_val = 1
    time.sleep(2)
    while True:
        key = input('Press key, then hit Enter. Enter q to exit: ')
        if key == 'f':
            print('Flipping Vertical Orientation...')
            flipVerticalOrient()
        if key == 'i':
            print('Changing ISO of the Camera...')
            setISOofCamera()
        if key == 'p':
            print('Taking Picture...')
            savePhotoToFile(img_val)
            print('Taking YUV array...')
            captureYUVArray(img_val)
            img_val += 1
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
import random

def info():
    '''Prints a basic library description'''
    print('Software library for the SmartCabinet project.')

def cameraSetup():
    print("Camera set up successfully!")
    return True

def turnOnCamera():
    print("Camera turned on!")
    
def identifyFace():
    '''The faceIdentified is a placeholder for when we implement a system to detect faces'''
    print("This is the person taking candy from the container!")
    faceIdentified = bool(random.choice([True, False]))
    return faceIdentified
    
def takePictureOfFace():
    faceThere = identifyFace()
    if faceThere = True:
        print("Photo taken!")
    else:
        print("No photo taken...")
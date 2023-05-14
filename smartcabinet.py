from global_ import userEntry, img_val, referenceUnit, overallAccessLog, keypadComboList, AccessAmount, rfidTags
from fractions import Fraction
from mfrc522 import SimpleMFRC522

import random, math, time, sys, picamera
import RPi.GPIO as GPIO

def info():
    #Prints a basic library description
    print('Software library for the SmartCabinet project.')

def cameraSetup(camera):
    '''
    This is used to set up the properties of the PiCamera
    Settings can be changed through editing the fucntions themselves
    '''
    camera.resolution = (640, 480)
    camera.framerate = 24
    camera.iso = 400
    camera.vflip = True             # Camera is upside down, so get it rightside-up
    time.sleep(2)
    print("Camera set up successfully!")

    # Starts the camera itself
    camera.start_preview()
    time.sleep(2)
    print("Camera turned on!")
    return camera

def savePhotoToFile(img_counter, nightModeVal, camera):
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
    print("Photo Taken")
    return camera

def flipVerticalOrient(camera):
    camera.vflip = not camera.vflip
    return camera

def setISOofCamera(camera):
    while True:
        try:
            isovalue = int(input('Enter an ISO value between 0 and 1600. 0 will set it to AUTO:'))
            if (isovalue < 0) or (isovalue > 1600):
                raise ValueError
            camera.iso = isovalue
            return camera
        except ValueError:
            print('Integers only please! If you did enter an integer, it was an illegal value!')
            continue

def setFramerateofCamera(camera):
    while True:
        try:
            framerateVal = int(input('Enter an framerate value:'))
            if (framerateVal < 0) or (framerateVal > 60):
                raise ValueError
            camera.framerate = framerateVal
            return camera
        except ValueError:
            print('Integers only please! If you did enter an integer, it was an illegal value!')
            continue

def nightModeSet(nightModeVal, camera):
    '''
    Asks to set night mode or not. Predetermined settings for night mode shown below.

    Adapted and restructured from:
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
            return nightModeVal, camera
        except ValueError:
            print('Integers only please! If you did enter an integer, it was an illegal value!')
            continue

def useCamera(thisFunctionCall = True):
    '''
    While the camera is turned on, we can perform various properties, such as taking pictures and even
    being to change its properties on the fly.

    otherFunctionCall will be used to see if other functions call this function.
    Default value of False
    '''
    global img_val
    nightModeBit = 0
    time.sleep(2)

    # Commented out as Pi Camera doesn't function for us
    # if camera:
    #     break
    # else:
    #     camera = picamera.PiCamera()
    # cameraSetup(camera)
    while True:
        if thisFunctionCall == False:
            print("Taking picture, then returning to previous function...")
            # camera = savePhotoToFile(img_val, nightModeBit, camera)
            img_val += 1
            # camera.close()
            return
        key = input('Press key, then hit Enter. Enter p to snap a photo. Enter q to exit: ')
        if key == 'f':
            print('Flipping Vertical Orientation...')
            # camera = flipVerticalOrient(camera)
        if key == 'i':
            print('Changing ISO of the Camera...')
            # camera = setISOofCamera(camera)
        if key == 'p':
            print('Taking Picture...')
            # camera = savePhotoToFile(img_val, nightModeBit, camera)
            img_val += 1
        if key == 'n':
            print('Night Mode Activate...')
            # nightModeBit, camera = nightModeSet(nightModeBit, camera)
        if key == 'r':
            print('Setting framerate...')
            # camera = setFramerateofCamera(camera)
        if key == 'q':
            print('Quitting Camera...')
            # camera.stop_preview()
            # camera.close()
            break


''' Keypad Portion '''

def keypadGPIOSetup():
    '''
    GPIO Pins are shown for the keypad
    '''
    R1 = 12
    R2 = 16
    R3 = 20
    R4 = 21

    C1 = 13
    C2 = 19
    C3 = 26
    return R1, R2, R3, R4, C1, C2, C3

def pinGPIOSetup(R1, R2, R3, R4, C1, C2, C3):
    '''
    Setup the GPIO pins and properties here
    '''
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

    print("Setup complete")

def readKeypadLine(line, characters, C1, C2, C3):
    '''
    The readKeypadLine function implements the procedure discussed in the article
    It sends out a single pulse to one of the rows of the keypad
    and then checks each column for changes.
    If it detects a change, the user pressed the button that connects the given line
    to the detected column

    Article: https://www.digikey.com/en/maker/blogs/2021/how-to-connect-a-keypad-to-a-raspberry-pi
    '''
    global userEntry
    correctKey = ["1", "2", "3", "4"]
    crtKeyStr = ""
    userKeyStr = ""
    for val in correctKey:
        crtKeyStr += val

    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        print(characters[0])
        userEntry.append(characters[0])
        print("User Entry so far: ", userEntry)
    if(GPIO.input(C2) == 1):
        print(characters[1])
        userEntry.append(characters[1])
        print("User Entry so far: ", userEntry)
    if(GPIO.input(C3) == 1):
        print(characters[2])
        userEntry.append(characters[2])
        print("User Entry so far: ", userEntry)
    GPIO.output(line, GPIO.LOW)

    # When 4 or more keys are entered, we take an appropriate action if it matches.
    if len(userEntry) == 4:
        successFlag = False
        for val in userEntry:
            userKeyStr += val
        print("User Entry: ", userKeyStr)
        print("Correct key: ", crtKeyStr)
        # Iterate through the list of keypad combos for workers
        for user, keyCode in keypadComboList.items():
            print("Keycode {code} for {user}".format(code=keyCode, user=user))
            if userKeyStr == str(keyCode):
                # If found, we welcome the user, and set a success flag.
                # Increase the value of accesses by one, and finally,
                # we must update the overallAccessLog, for the user
                print("Welcome {user}!".format(user=user))
                AccessAmount[user] += 1
                for logEntry in overallAccessLog:
                    #print("Log Entry: ", logEntry['Person'])
                    if logEntry['Person'] == user:
                        print("New val: ", AccessAmount[user])
                        print("Print Value: ", logEntry['Times Accessed'])
                        logEntry['Times Accessed'] = "{accessAmount} at {currentDateTime}".format(accessAmount=AccessAmount[user], currentDateTime=time.strftime("%m/%d/%Y, %H:%M:%S"))
                        print("Print New Value: ", logEntry['Times Accessed'])
                        break
                successFlag = True
            # Break out of loop if we succeeeded in finding someone.
            if successFlag == True:
                break
        if successFlag == True:
            print("Unlocked")
            servoOperate(1)
        else:
            print("Wrong keycode! Try again")
            servoOperate(0)
        userEntry.clear()

    elif len(userEntry) >= len(correctKey):
        print("Somehow entered more than 4 characters")
        userEntry.clear()

def keypadOperate():
    '''
    Reads the inputs of the keypad and determines if the manager can access the site
    '''
    print("keypadOperate running!")
    # Redefine the pins if necessary by calling this function and changing the pins from there.
    R1, R2, R3, R4, C1, C2, C3 = keypadGPIOSetup()
    pinGPIOSetup(R1, R2, R3, R4, C1, C2, C3)

    print("back to keypadOperate")

    try:
        while True:
            # call the readKeypadLine function for each row of the keypad
            readKeypadLine(R1, ["1","2","3"], C1, C2, C3)
            readKeypadLine(R2, ["4","5","6"], C1, C2, C3)
            readKeypadLine(R3, ["7","8","9"], C1, C2, C3)
            readKeypadLine(R4, ["*","0","#"], C1, C2, C3)
            time.sleep(0.15)
    except KeyboardInterrupt:
        print("\nApplication stopped!")

''' Servo Portion '''

def servoSetup():
    '''
    Sets up the servo, before returning to the previous function.
    '''
    print("Setting up servo!")
    GPIO.setwarnings(False)
    servoPIN = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50)      # GPIO 18 for PWM with 50Hz
    p.start(2.5)                    # Initialization
    time.sleep(2)

    return p

def lockCabinet(p):
    '''
    Locks the cabinet
    '''
    p.ChangeDutyCycle(2.5)

def unlockCabinet(p):
    '''
    Locks the cabinet
    '''
    p.ChangeDutyCycle(12.5)

def servoOperate(state):
    '''
    Opeartes the servo, runs once.

    1 = Unlock
    
    0 = Lock

    Adapted and restructured from:
    https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/
    '''
    p = servoSetup()

    try:
        if state == 1:
            unlockCabinet(p)
            time.sleep(0.5)
        elif state == 0:
            lockCabinet(p)
            time.sleep(0.5)
        else:
            print("Invalid state")
        p.stop()
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()

''' RFID Portion '''

def rfidSetup():
    '''
    Sets up the RFID chip
    '''
    print("Setting up RFID")
    reader = SimpleMFRC522()
    print("RFID Setup Complete!")
    return reader

def rfidOperate():
    '''
    Reads the RFID chip and cards
    '''
    reader = rfidSetup()
    print("Hold a tag near the reader")
    print("Reading tag in 3 seconds...")
    time.sleep(3)

    # Keep it for now. We only want it to run if the user calls for it from the browser UI.
    id = reader.read_id_no_block()
    
    try:
        while True:
            id = reader.read_id_no_block()
            if id:
                print(hex(id))
                servoOperate(1)
                for user, rfidCode in rfidTags.items():
                    print("Keycode {code} for {user}".format(code=rfidCode, user=user))
                    if str(hex(id)) == str(rfidCode):
                        # If found, we welcome the user, and set a success flag.
                        # Increase the value of accesses by one, and finally,
                        # we must update the overallAccessLog, for the user
                        print("Welcome {user}!".format(user=user))
                        AccessAmount[user] += 1
                        for logEntry in overallAccessLog:
                            #print("Log Entry: ", logEntry['Person'])
                            if logEntry['Person'] == user:
                                print("New val: ", AccessAmount[user])
                                print("Print Value: ", logEntry['Times Accessed'])
                                logEntry['Times Accessed'] = "{accessAmount} at {currentDateTime}".format(accessAmount=AccessAmount[user], currentDateTime=time.strftime("%m/%d/%Y, %H:%M:%S"))
                                print("Print New Value: ", logEntry['Times Accessed'])
                        break
                # Ten seconds for the bowl to stay open
                time.sleep(10)
                servoOperate(0)
            else:
                print("No tag detected")
            time.sleep(3)
    except KeyboardInterrupt:
        GPIO.cleanup()

''' Load Cell Portion '''

def cleanAndExit(EMULATE_HX711):
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()

def loadCellWeightMeasure(hx):
    '''
    We continuously measure the weight of the object above us.
    '''
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
    time.sleep(1)

def loadCellCalibration(approxWeightValue, loadCellReading):
    '''
    Should only be called from the website
    '''
    global referenceUnit
    referenceUnit = 1

    time.sleep(5)

    referenceUnit = loadCellReading/approxWeightValue

def loadCellOperate():
    '''
    We set up the load cell
    '''
    EMULATE_HX711 = False
    
    global referenceUnit

    if not EMULATE_HX711:
        from hx711 import HX711
        print("Not emualated")
    else:
        from emulated_hx711 import HX711
        print("Emulated")

    hx = HX711(5, 6) # GPIO Pins 5 and 6
    hx.set_reading_format("MSB", "MSB")

    # HOW TO CALCULATE THE REFFERENCE UNIT
    # To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
    # In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
    # and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
    # If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
    #hx.set_reference_unit(113)
    referenceUnit = 451       # Reference Value of Tommy's Phone
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()
    print("Tare done! Add weight now...")
    
    while True:
        try:
            loadCellWeightMeasure(hx)
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit(EMULATE_HX711)
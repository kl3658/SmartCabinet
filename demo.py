#from smartcabinet import info, keypadOperate
import smartcabinet

print("Info going!")
smartcabinet.info()
print("Info gone!")
#smartcabinet.cameraSetup()
#smartcabinet.turnOnCamera()

# Used to test out the identifyFace function
#smartcabinet.useCamera()

# Test out the keypad
print("Keypad coming!")
smartcabinet.keypadOperate()
print("Keypad Gone!")

# Test out the servo
print("Servo coming!")
smartcabinet.servoOperate()
print("Servo gone!")

# Test out the RFID
print("RFID coming!")
smartcabinet.rfidOperate()
print("RFID gone!")

print("Load Cell Incoming!")
smartcabinet.loadCellOperate()
print("Load Cell gone!")

import smartcabinet
from threading import Thread

'''
print("Info going!")
smartcabinet.info()
print("Info gone!")

# Used to test out the camera
smartcabinet.useCamera()

# Test out the keypad
print("Keypad coming!")
smartcabinet.keypadOperate()
print("Keypad Gone!")

# Test out the servo
print("Servo coming!")
smartcabinet.servoOperate(1)
print("Servo gone!")

# Test out the RFID
print("RFID coming!")
smartcabinet.rfidOperate()
print("RFID gone!")

print("Load Cell Incoming!")
smartcabinet.loadCellOperate()
print("Load Cell gone!")
'''

# We really only need about 4 threads. One for:
# Camera, Keypad, RFID, and the Load Cell.
# Servo isn't included as its called via other functions.
cameraThread = Thread(target = smartcabinet.useCamera(), daemon=True)
cameraThread.start()
keypadThread = Thread(target = smartcabinet.keypadOperate(), daemon=True)
keypadThread.start()
rfidThread = Thread(target = smartcabinet.rfidOperate(), daemon=True)
rfidThread.start()
loadCellThread = Thread(target = smartcabinet.loadCellOperate(), daemon=True)
loadCellThread.start()
cameraThread.join()
keypadThread.join()
rfidThread.join()
loadCellThread.join()
#from smartcabinet import info, keypadOperate
import smartcabinet

print("Info going!")
smartcabinet.info()
print("Info gone!")
smartcabinet.cameraSetup()
smartcabinet.turnOnCamera()

# Used to test out the identifyFace function
smartcabinet.useCamera()

# Test out the keypad
print("Keypad coming!")
smartcabinet.keypadOperate()

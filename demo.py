import smartcabinet
from threading import Thread

# We really only need about 4 threads. One for:
# Camera, Keypad, RFID, and the Load Cell.
# Servo isn't included as its called via other functions.
cameraThread = Thread(target = smartcabinet.useCamera)
cameraThread.start()
keypadThread = Thread(target = smartcabinet.keypadOperate)
keypadThread.start()
rfidThread = Thread(target = smartcabinet.rfidOperate)
rfidThread.start()
loadCellThread = Thread(target = smartcabinet.loadCellOperate)
loadCellThread.start()
# cameraThread.join()
# keypadThread.join()
# rfidThread.join()
# loadCellThread.join()
import smartcabinet
import time

smartcabinet.cameraSetup()
smartcabinet.turnOnCamera()

# Used to test out the identifyFace function
smartcabinet.useCamera()

# We could test this function out 3 times, which calls identifyFace in turn
smartcabinet.savePhotoToFile(1)
smartcabinet.savePhotoToFile(2)
smartcabinet.savePhotoToFile(3)
import smartcabinet
import time

smartcabinet.cameraSetup()
smartcabinet.turnOnCamera()

# Used to test out the identifyFace function
smartcabinet.identifyFace()

# We could test this function out 3 times, which calls identifyFace in turn
smartcabinet.takePictureOfFace()
smartcabinet.takePictureOfFace()
smartcabinet.takePictureOfFace()
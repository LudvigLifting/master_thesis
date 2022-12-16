from time import sleep
from picamera import PiCamera

camera = PiCamera()

camera.resolution = (200, 200)
camera.start_preview()
sleep(2)
camera.capture("test2.jpg")
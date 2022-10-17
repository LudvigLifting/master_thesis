from time import sleep
from picamera import PiCamera

camera = PiCamera()

camera.resolution = (500, 500)
camera.start_preview()
sleep(2)
camera.capture("test.jpg")
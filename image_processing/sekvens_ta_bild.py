from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.color_effects = None #(128, 128) #svartvit
resolutions = [(50*i, 50*i) for i in range(1, 11)]
print(f"Resolutions: {resolutions}")

for resolution in resolutions:
    camera.resolution = resolution
    camera.start_preview()
    sleep(2)
    camera.capture("test_color" + str(resolution[0]) + "x" + str(resolution[1]) + ".jpg")
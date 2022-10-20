from time import sleep
from picamera import PiCamera        

camera = PiCamera()
camera.color_effects = None #(128, 128) #svartvit
resolutions = [(50*i, 50*i) for i in range(1, 11)]
print(f"Resolutions: {resolutions}")


camera.start_preview(fullscreen=False, window=(100, 20, 1000, 1000))
sleep(5)
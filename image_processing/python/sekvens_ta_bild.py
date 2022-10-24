from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.color_effects = (128, 128) #svartvit
resolutions = [(50*i, 50*i) for i in range(1, 7)]
print(f"Resolutions: {resolutions}")
dir_path = "/home/exjobb/code/master_thesis/image_processing/pictures/" 

for resolution in resolutions:
    camera.resolution = resolution
    #camera.start_preview()
    sleep(0.2)
    camera.capture(dir_path + "ext1/" + str(resolution[0]) + "x" + str(resolution[1]) + ".jpg")
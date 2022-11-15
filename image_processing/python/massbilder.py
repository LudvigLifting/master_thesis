from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.color_effects = (128, 128) #svartvit
resolution = (200, 200)
dir_path = "/home/exjobb/code/master_thesis/image_processing/pictures/many/" 

nbr_images = 10
for i in range(nbr_images):
    print(f"image {i}")
    camera.resolution = resolution
    sleep(0.2)
    camera.capture(dir_path + str(i) + ".jpg")
    print("done")
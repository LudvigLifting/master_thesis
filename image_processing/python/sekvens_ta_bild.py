from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.color_effects = (128, 128) #svartvit
resolution = (200, 200)
dir_path = "/home/exjobb/code/master_thesis/image_processing/" 

nbr_images = 200
for i in range(101, 202):
    print(f"image {i}")
    camera.resolution = resolution
    sleep(2)
    if i == 101:
        camera.capture(dir_path + "ref2" + ".jpg")
    else: 
        camera.capture(dir_path + str(i) + ".jpg")
    print("done")

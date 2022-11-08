from email.mime import image
from cv2 import threshold
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import time
import pathlib
import math


def adaptive_threshold(dir_path, files):

    #for file in files:
    file = files[5]
    resultimage = np.zeros((800, 800))
    
    ex1 = cv2.imread(dir_path + "1" + file)
    ex2 = cv2.imread(dir_path + "2" + file)
   # ex1 = cv2.normalize(ex1, resultimage, 0, 1, cv2.NORM_MINMAX)
    
    plt.figure(file)
    sub1 = plt.subplot(2, 2, 1)
    plt.imshow(ex1)
   # ex2 = cv2.normalize(ex2, resultimage, 0, 1, cv2.NORM_MINMAX)
    sub2 = plt.subplot(2, 2, 2)
    plt.imshow(ex2)
    diff1 =cv2.subtract(ex1, ex2)
    sub3 = plt.subplot(2, 2, 3)
    plt.imshow(diff1)
    diff2 = cv2.subtract(ex2, ex1)
    sub4 = plt.subplot(2, 2, 4)
    plt.imshow(diff2)

    sub1.title.set_text(f'norm1')
    sub2.title.set_text(f'norm2')
    sub3.title.set_text(f'diff1')
    sub4.title.set_text(f'diff2')
    plt.show()

def histo(image: np.ndarray, name: str=""):

    plt.figure(f"Histogram of {name}")
    flattened = np.ravel(image)
    plt.hist(flattened, len(flattened))
    if name == "":
        plt.title("Histogram")
    else:
        plt.title(name)
    plt.xlabel("Pixel")
    plt.ylabel("Intensity")

def simple_threshold(dir_path: str, files: list):
    for file in files:
        image = cv2.imread(dir_path + files[5])

        plt.figure(file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        #Changing size
        (rows, cols) = gray.shape
        
        cut = round(rows*0.7)
        gray = gray[0:cut]
        gray = np.array([row[round((rows-cut)/2):cols-round((rows-cut)/2)] for row in gray])
        
        print(gray.shape)


        sobel_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=1)
        #sobel_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=1)
        
        sub1 = plt.subplot(2, 3, 1)
        plt.imshow(sobel_x, cmap="gray")
        
        #Normalize
        t10 = cv2.threshold(sobel_x, 10, 255, cv2.THRESH_BINARY)[1]
        t30 = cv2.threshold(sobel_x, 30, 255, cv2.THRESH_BINARY)[1]
        t50 = cv2.threshold(sobel_x, 50, 255, cv2.THRESH_BINARY)[1]
        t60 = cv2.threshold(sobel_x, 60, 255, cv2.THRESH_BINARY)[1]
        t70 = cv2.threshold(sobel_x, 70, 255, cv2.THRESH_BINARY)[1]
        
        sub2 = plt.subplot(2, 3, 2)
        plt.imshow(t10, cmap="gray")
        sub3 = plt.subplot(2, 3, 3)
        plt.imshow(t30, cmap="gray")
        sub4 = plt.subplot(2, 3, 4)
        plt.imshow(t50, cmap="gray")
        sub5 = plt.subplot(2, 3, 5)
        plt.imshow(t60, cmap="gray")
        sub6 = plt.subplot(2, 3, 6)
        plt.imshow(t70, cmap="gray")
    
        sub1.title.set_text(f'Sobel x original')
        sub2.title.set_text(f'Threshold value 10')
        sub3.title.set_text(f'Threshold value 30')
        sub4.title.set_text(f'Threshold value 50')
        sub5.title.set_text(f'Threshold value 60')
        sub6.title.set_text(f'Threshold value 70')

        #plt.tight_layout()
        plt.subplots_adjust(
            top=0.965,
            bottom=0.0,
            left=0.13,
            right=0.9,
            hspace=0.225,
            wspace=0.14)
        break
    plt.show()
    time.sleep(60)
    plt.close()
    
def pixelcalc():
    
    A = (((25*10**(-3))/2)**2)*math.pi
    pixel_widths = [50+i for i in range(1,450)]
    pixel_sizes = [(A/(w**2))*700000 for w in pixel_widths]
    plt.plot(pixel_widths, [size**2 for size in pixel_sizes])
    plt.xlabel("nbr pixels")
    plt.ylabel("size [mm^2]")
    plt.title("Function of pixel size depending on resolution")
    plt.show()
    
def diff(image1: np.ndarray, image2: np.ndarray):
    
    return np.array([[abs(int(val1) - int(val2)) for val1, val2 in zip(row1, row2)] for row1, row2 in zip(image1, image2)], dtype=np.uint8) 

def adaptive(arr: np.ndarray, value: np.uint8, type_th: str="mean"):

    if type_th == "mean":
        return np.uint8(255) if value > np.uint8(sum(arr)/len(arr)) else np.uint8(0)
    elif type_th == "median":
        return np.sort(arr, 1)[round((len(arr)-1)/2)]
    
def sobel_threshold(image: np.ndarray, type_ba: str="basic"):
    
    ret_arr = []
    
    #Change size to isolate pekare
    # (rows, cols) = image.shape
    # cut = round(rows*0.55)
    # image = image[round(cut/4):cut]
    # image = np.array([row[round(cut/2):cols - round(cut/2) -1] for row in image])
    
    #Sobel on image
    image = cv2.Sobel(image, cv2.CV_8U, 1, 0, ksize=1)
    
    th_scheme = "mean"
    
    if type_ba == "basic":
        #basic globalthresholding
        for cutoff in range(10, 40, 10):
            ret_arr.append(cv2.threshold(image, cutoff, 255, cv2.THRESH_BINARY)[1])
        print(ret_arr)
        return ret_arr
    else:
        #advanced adaptive thresholding (3x3)
        (rows, cols) = image.shape
        print(image.shape)
        flattened = np.ravel(image)
        for i in range(len(flattened)):
            if i < cols:
                #top row
                if cols - i % cols == 1:
                    #right edge
                    subarray = np.concatenate((flattened[i-1:i], flattened[i+cols-1:i+cols]))
                elif i % cols == 0:
                    #left edge
                    subarray = np.concatenate((flattened[i:i+1], flattened[i+cols:i+cols+1]))
                else:
                    subarray = np.concatenate((flattened[i-1:i+1], flattened[i+cols-1:i+cols+1]))
            elif i > rows*(cols -1):
                #bottom row
                if cols - i % cols == 1:
                    #right edge
                    subarray = np.concatenate((flattened[i-cols-1:i-cols], flattened[i-1:i]))
                elif i % cols == 0:
                    #left edge
                    subarray = np.concatenate((flattened[i-cols:i-cols+1], flattened[i:i+1]))
                else:
                    subarray = np.concatenate((flattened[i-cols-1:i-cols+1], flattened[i-1:i+1]))
            else:
                #Normal
                if cols - i % cols == 1:
                    #right edge
                    subarray = np.concatenate((flattened[i-cols-1:i-cols], flattened[i-1:i], flattened[i+cols-1:i+cols]))
                elif i % cols == 0:
                    #left edge
                    subarray = np.concatenate((flattened[i-cols:i-cols+1], flattened[i:i+1], flattened[i+cols:i+cols+1]))
                else:
                    subarray = np.concatenate((flattened[i-cols-1:i-cols+1], flattened[i-1:i+1], flattened[i+cols-1:i+cols+1]))
            if i < cols:
                image[0][i] = adaptive(subarray, flattened(i), th_scheme)
            else:
                #print(f"shape = {image.shape}, i = {i}, row = {round((i-i%rows)/rows)}, col = {i%(rows)}")
                image[round((i-i%rows)/rows)][i%(rows)] = adaptive(subarray, th_scheme)
        return image
                    
                    

def main():
    dir_path = str(pathlib.Path(__file__).parent.resolve())
    folder = ["/../pictures/ext1", "/../pictures/ext2"]
    files = [
        "/50x50.jpg",
        "/100x100.jpg",
        "/150x150.jpg",
        "/200x200.jpg",
        "/250x250.jpg",
        "/300x300.jpg"
    ]
    
    #Load images
    images = [[] for _ in range(len(folder))]
    for i in range(len(folder)):
        for file in files:
            image = cv2.imread(dir_path + folder[i] + file)
            print(dir_path + file)
            images[i].append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    
    # #Histograms for the images
    # for i, image in enumerate(images):
    #     histo(image[5], f"Image {i + 1} res: {files[5][1:len(files[5])-4]}")
    
    #threshold = (sobel_threshold(images[0][0], "advanced"))
    #time.sleep(10)
    
    #Thresholding on the images for all resolutions
    thresholds = [[[] for _ in range(len(images[0]))] for _ in range(len(images))]
    for i, image in enumerate(images):
        for j, res in enumerate(image):
            thresholds[i][j] = (sobel_threshold(res, "basic"))
            
        
    #Generate and plot diff images
    res = 5
    for i in range(0, len(thresholds), 2):
        for j, (image1, image2) in enumerate(zip(thresholds[i][res], thresholds[i+1][res])):
            plt.figure(f"diff of image {i} and {i+1} size = {image1.shape} and threshold {j*10 + 10}")
            difference = diff(image1, image2)
            #print(image1)
            
            sub = plt.subplot(3, 1, 1)
            plt.imshow(image1, cmap="gray")
            sub.title.set_text(f'Image 1')
            sub = plt.subplot(3, 1, 2)
            plt.imshow(image2, cmap="gray")
            sub.title.set_text(f'Image 2')
            sub = plt.subplot(3, 1, 3)
            plt.imshow(difference, cmap="gray")
            sub.title.set_text(f'Diff image (diff = 1 - 2)')
    plt.show()
        
    

if __name__ == '__main__':
    main()
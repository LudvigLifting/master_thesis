from email.mime import image
from cv2 import threshold
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import time
import pathlib
import math

def histo(image: np.ndarray, name: str="") -> None:

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
    
def pixelcalc() -> None:
    
    A = (((25*10**(-3))/2)**2)*math.pi
    pixel_widths = [50+i for i in range(1,450)]
    pixel_sizes = [(A/(w**2))*700000 for w in pixel_widths]
    plt.plot(pixel_widths, [size**2 for size in pixel_sizes])
    plt.xlabel("nbr pixels")
    plt.ylabel("size [mm^2]")
    plt.title("Function of pixel size depending on resolution")
    plt.show()
    
def diff(image1: np.ndarray, image2: np.ndarray) -> np.ndarray:
    
    return np.array([[abs(int(val1) - int(val2)) for val1, val2 in zip(row1, row2)] for row1, row2 in zip(image1, image2)], dtype=np.uint8) 

def adaptive(arr: np.ndarray, value: np.uint8, C: int=0, type_th: str="mean") -> np.uint8:

    if type_th == "mean":
        return np.uint8(255) if value > np.uint8(sum(arr)/len(arr)) + C else np.uint8(0)
    elif type_th == "median":
        return np.sort(arr, 1)[round((len(arr)-1)/2)]

def sub_3x3(flattened: np.ndarray, i: int, shape: tuple) -> np.ndarray:

    (rows, cols) = shape
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
    return subarray

def filter_dots(image: np.ndarray, level: int) -> np.ndarray:
    
    (rows, cols) = image.shape
    flattened = np.ravel(image)
    for i in range(len(flattened)):
        if flattened[i] != 0:
            sub = sub_3x3(flattened, i, (rows, cols))
            #print(f"{sum(sub)}, {flattened[i]}")
            if sum(sub) <= level*flattened[i]:
                if i < cols:
                    #First row
                    image[0][i] = np.uint8(0)
                else:
                    #All other rows
                    image[round((i-i%rows)/rows)][i%(rows)] = np.uint8(0)            
    
    return image

def scale_light(image1: np.ndarray, image2: np.ndarray) -> np.ndarray:
    
    im1 = image1.copy()
    im2 = image2.copy()
    #Loop over image to find max/min value
    (max1, max2) = (np.max(im1), np.max(im2))
    (min1, min2) = (np.min(im1), np.min(im2))
    print(f"Max = {max1 }, {max2}, Min = {min1 }, {min2}")
    mean1 = int(np.sum(im1)/(im1.shape[0]*im1.shape[1]) - 50)
    mean2 = int(np.sum(im2)/(im2.shape[0]*im2.shape[1]) - 50)
    print(f"mean1 {mean1}, mean2 {mean2}")
    
    #Scale images
    im1 = np.reshape(np.array([np.uint8(pixel*(mean2/mean1) if pixel*(mean2/mean1) < 255 else 255) for pixel in np.ravel(im1)]), image1.shape)
    im2 = np.reshape(np.array([np.uint8(pixel*(mean1/mean2) if pixel*(mean1/mean2) < 255 else 255) for pixel in np.ravel(im2)]), image2.shape)
    
    return np.array([im1, im2])

def crop(image: np.ndarray, percentage: int, ratio: int=1) -> np.ndarray:
    
    #ratio is row/col
    #percentage is % of rows/cols to remove
    cropped = image.copy()
    (rows, cols) = image.shape
    #How many to take away
    cutRow = round(rows*(percentage/100)*ratio)
    cutCol = round(cols*(percentage/100)*(1/ratio))
    cropped = cropped[round(cutRow/2):rows - round(cutRow/2) - 1]
    cropped = np.array([row[round(cutCol/2):cols - round(cutCol/2) - 1] for row in cropped])
    
    return cropped

def pad(image: np.ndarray) -> np.ndarray:

    cols = image.shape[1]
    padded = []
    padded.append(np.zeros((1, cols + 2), np.uint8))
    for row in image:
        padded.append(np.concatenate((np.zeros(1, np.uint8), row, np.zeros(1, np.uint8))))
    padded.append(np.zeros((1, cols + 2), np.uint8))
    
    return np.array(padded)
    
def sobel_threshold(image: np.ndarray, type_ba: str="basic") -> np.ndarray:
    
    #Sobel on image
    sobel = cv2.Sobel(image, cv2.CV_8U, 1, 0, ksize=3)
    
    th_scheme = "mean"
    
    if type_ba == "global":
        ret_arr = []
        #basic globalthresholding
        for cutoff in range(10, 40, 10):
            ret_arr.append(cv2.threshold(sobel, cutoff, 255, cv2.THRESH_BINARY)[1])
        return ret_arr
    else:
        #advanced adaptive thresholding (3x3)
        (rows, cols) = sobel.shape
        flattened = np.ravel(sobel)
        offset = 20
        for i in range(len(flattened)):
            if i < cols:
                #First row
                sobel[0][i] = adaptive(sub_3x3(flattened, i, (rows, cols)), flattened[i], offset, th_scheme)
            else:
                #All other rows
                sobel[round((i-i%rows)/rows)][i%(rows)] = adaptive(sub_3x3(flattened, i, (rows, cols)), flattened[i], offset, th_scheme)
        return sobel                  

def main():
    dir_path = str(pathlib.Path(__file__).parent.resolve())
    folder = ["/../pictures/ext" + str(n) for n in range(4)]
    files = [
        "/50x50.jpg",
        "/100x100.jpg",
        "/150x150.jpg",
        "/200x200.jpg",
        "/250x250.jpg",
        "/300x300.jpg"
    ]
    res = {
        "50x50"     : 0,
        "100x100"   : 1,
        "150x150"   : 2,
        "200x200"   : 3,
        "250x250"   : 4,
        "300x300"   : 5
    }
    
    #Load images
    images = [[] for _ in range(len(folder))]
    for i in range(len(folder)):
        for file in files:
            image = cv2.imread(dir_path + folder[i] + file)
            #print(dir_path + folder[i] + file)
            images[i].append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    pad(images[0][res["50x50"]])
    
    im = scale_light(images[0][res["300x300"]], images[1][res["300x300"]])
    plt.figure("test_light")
    sub = plt.subplot(3, 2, 1)
    plt.imshow(images[0][res["300x300"]], cmap="gray")
    sub.title.set_text(f'Image 1 original')
    sub = plt.subplot(3, 2, 2)
    plt.imshow(images[1][res["300x300"]], cmap="gray")
    sub.title.set_text(f'Image 2 original')
    sub = plt.subplot(3, 2, 3)
    plt.imshow(im[0], cmap="gray")
    sub.title.set_text(f'Image 1 scaled')
    sub = plt.subplot(3, 2, 4)
    plt.imshow(im[1], cmap="gray")
    sub.title.set_text(f'Image 2 scaled')
    
    diff1 = diff(images[0][res["300x300"]], im[0])
    diff2 = diff(images[1][res["300x300"]], im[1])
    sub = plt.subplot(3, 2, 5)
    plt.imshow(diff1, cmap="gray")
    sub.title.set_text(f'Image 1 diff')
    sub = plt.subplot(3, 2, 6)
    plt.imshow(diff2, cmap="gray")
    sub.title.set_text(f'Image 2 diff')
    plt.show()
    
    #Scale light in pairs of two         

    
    #Thresholding on the images for all resolutions
    thresholds = [[[] for _ in range(len(images[0]))] for _ in range(len(images))]
    for i, image in enumerate(images):
        for j, resolution in enumerate(image):
            thresholds[i][j] = sobel_threshold(resolution, "adaptive")
            
        
    #Generate and plot diff images
    for i in range(0, len(thresholds), 2):
        reso = "150x150"
        image1 = thresholds[i][res[reso]]
        image2 = thresholds[i+1][res[reso]]
        print(len(image1))
        plt.figure(f"diff of image {i} and {i+1} size = {len(image1)}x{len(image1[0])}")
        
        #Compute difference image
        difference = diff(image1, image2)
        nbr = int(np.sum(difference)/255)
        print(f"Number of white pixels: {nbr} = {nbr/(difference.shape[0]*difference.shape[1]):.3f}%")
        
        #Filter difference image
        filtered = filter_dots(difference.copy(), 1)
        
        #Save result images
        cv2.imwrite(f"{dir_path}/../pictures/test/diff_{i}.png", difference)
        cv2.imwrite(f"{dir_path}/../pictures/test/before_diff_img1.png", image1)
        cv2.imwrite(f"{dir_path}/../pictures/test/before_diff_img2.png", image2)
        cv2.imwrite(f"{dir_path}/../pictures/test/filter_diff_{i}.png", filtered)
        
        sub = plt.subplot(2, 2, 1)
        plt.imshow(image1, cmap="gray")
        sub.title.set_text(f'Image 1')
        sub = plt.subplot(2, 2, 3)
        plt.imshow(image2, cmap="gray")
        sub.title.set_text(f'Image 2')
        sub = plt.subplot(2, 2, 2)
        plt.imshow(difference, cmap="gray")
        sub.title.set_text(f'Diff image (diff = 1 - 2)')
        sub = plt.subplot(2, 2, 4)
        plt.imshow(filtered, cmap="gray")
        sub.title.set_text(f'Filtered diff level 1')
    plt.show()
        
    

if __name__ == '__main__':
    main()
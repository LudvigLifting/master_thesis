import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

def main():
    dir_path = "/home/exjobb/code/master_thesis/image_processing"
    file = "/test_color500x500.jpg"
    print(dir_path + file)

    fig = plt.figure()

    image_BGR = cv2.imread(dir_path + file, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image_BGR, cv2.COLOR_BGR2GRAY)
    #gray = cv2.imread(dir_path + "/test500x500.jpg", cv2.IMREAD_COLOR)
    #sub1 = plt.subplot(4, 2, 1)
    #plt.imshow(gray)
    
    
    sobel_x = cv2.Sobel(gray, 2, 1, 0, ksize=3, scale=1)
    sobel_y = cv2.Sobel(gray, 2, 0, 1, ksize=3, scale=1)
    sub2 = plt.subplot(2, 2, 1)
    plt.imshow(sobel_x)
    sub3 = plt.subplot(2, 2, 2)
    plt.imshow(sobel_y)
    #prewitt
    #robert = cv2.rober
    laplacian = cv2.Laplacian(gray, 2)
    sub4 = plt.subplot(2, 2, 3)
    plt.imshow(laplacian)

    canny = cv2.Canny(gray, 50, 100)
    sub5 = plt.subplot(2, 2, 4)
    plt.imshow(canny)

    #sub1.title.set_text('Original')
    sub2.title.set_text('Sobel x')
    sub3.title.set_text('Sobel y')
    sub4.title.set_text('Laplacian')
    sub5.title.set_text('Canny')
    plt.show()
    

if __name__ == '__main__':
    main()
from email.mime import image
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import time


def lol1(dir_path, files):

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

def histo(dir_path, files):
    for file in files:
        gray = cv2.imread(dir_path + "1" + file)

        plt.figure(file)
        resultimage = np.zeros((800, 800))

        sobel_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=1, scale=1)
        sobel_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=1, scale=1)

        sub1 = plt.subplot(2, 2, 1)
        plt.hist(np.ravel(sobel_x[0]))
        sub2 = plt.subplot(2, 2, 2)
        plt.hist(np.ravel(sobel_y[0]))

            
        # sobel_x = cv2.normalize(cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=1), resultimage, 0, 1, cv2.NORM_MINMAX)
        # sobel_y = cv2.normalize(cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=1), resultimage, 0, 1, cv2.NORM_MINMAX)
        #sobel_x = cv2.convertScaleAbs(sobel_x, resultimage, 0, 255)
        sobel_x = cv2.cvtColor(sobel_x, cv2.COLOR_BGR2GRAY)
        print(sobel_x.shape)
        sobel_x = cv2.adaptiveThreshold(sobel_x, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 73, 0)
        #sobel_y = cv2.convertScaleAbs(sobel_y, resultimage, 0, 255)
        sobel_y = cv2.cvtColor(sobel_y, cv2.COLOR_BGR2GRAY)
        sobel_y = cv2.adaptiveThreshold(sobel_y, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 73, 0)
        sub3 = plt.subplot(2, 2, 3)
        plt.hist(np.ravel(sobel_x))
        sub4 = plt.subplot(2, 2, 4)
        plt.hist(np.ravel(sobel_x))
    

        #sub1.title.set_text('Original')
        sub1.title.set_text(f'Sobel x')
        sub2.title.set_text(f'Sobel y')
        sub3.title.set_text(f'Sobel x norm')
        sub4.title.set_text(f'Sobel y norm')


        #plt.tight_layout()
        plt.subplots_adjust(
            top=0.965,
            bottom=0.0,
            left=0.13,
            right=0.9,
            hspace=0.225,
            wspace=0.14)
    plt.show()
    time.sleep(10)
    plt.close()

def lol(dir_path, files):
    for file in files:
        gray = cv2.imread(dir_path + "1" + file)

        plt.figure(file)
        resultimage = np.zeros((800, 800))
        # for i in range(1, 6, 2):
        #     sobel_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=i, scale=1)
        #     sobel_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=i, scale=1)
        #     # sobel_x = cv2.normalize(cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=i), resultimage, 0, 1, cv2.NORM_MINMAX)
        #     # sobel_y = cv2.normalize(cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=i), resultimage, 0, 1, cv2.NORM_MINMAX)
        #     sub2 = plt.subplot(4, 2, i)
        #     plt.imshow(sobel_x, cmap="gray")
        #     sub3 = plt.subplot(4, 2, i+1)
        #     plt.imshow(sobel_y, cmap="gray")
        

        #     #sub1.title.set_text('Original')
        #     sub2.title.set_text(f'Sobel x with kernel size {i}')
        #     sub3.title.set_text(f'Sobel y with kernel size {i}')


        sobel_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=1, scale=1)
        sobel_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=1, scale=1)

        sub1 = plt.subplot(2, 2, 1)
        plt.imshow(sobel_x, cmap="gray")
        sub2 = plt.subplot(2, 2, 2)
        plt.imshow(sobel_y, cmap="gray")

            
        # sobel_x = cv2.normalize(cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=1), resultimage, 0, 1, cv2.NORM_MINMAX)
        # sobel_y = cv2.normalize(cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=1), resultimage, 0, 1, cv2.NORM_MINMAX)
        #sobel_x = cv2.convertScaleAbs(sobel_x, resultimage, 0, 255)
        sobel_x = cv2.cvtColor(sobel_x, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.adaptiveThreshold(sobel_x, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 253, 0)
        #sobel_y = cv2.convertScaleAbs(sobel_y, resultimage, 0, 255)
        sobel_y = cv2.cvtColor(sobel_y, cv2.COLOR_BGR2GRAY)
        sobel_y = cv2.adaptiveThreshold(sobel_y, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 253, 0)
        sub3 = plt.subplot(2, 2, 3)
        plt.imshow(sobel_x, cmap="gray")
        sub4 = plt.subplot(2, 2, 4)
        plt.imshow(sobel_y, cmap="gray")
    

        #sub1.title.set_text('Original')
        sub1.title.set_text(f'Sobel x')
        sub2.title.set_text(f'Sobel y')
        sub3.title.set_text(f'Sobel x norm')
        sub4.title.set_text(f'Sobel y norm')


        #plt.tight_layout()
        plt.subplots_adjust(
            top=0.965,
            bottom=0.0,
            left=0.13,
            right=0.9,
            hspace=0.225,
            wspace=0.14)
    plt.show()
    time.sleep(60)
    plt.close()


    """
    top=0.965,
    bottom=0.0,
    left=0.13,
    right=0.9,
    hspace=0.225,
    wspace=0.14
    """

def main():
    dir_path = "/home/exjobb/code/master_thesis/image_processing/pictures/ext"
    files = [
        "/50x50.jpg",
        "/100x100.jpg",
        "/150x150.jpg",
        "/200x200.jpg",
        "/250x250.jpg",
        "/300x300.jpg"
    ]

    lol(dir_path, files)
    #cv2.cvtColor(image_BGR, cv2.COLOR_BGR2GRAY)

    #gray = cv2.imread(dir_path + "/test500x500.jpg", cv2.IMREAD_COLOR)
    #sub1 = plt.subplot(4, 2, 1)
    #plt.imshow(gray)
    

if __name__ == '__main__':
    main()
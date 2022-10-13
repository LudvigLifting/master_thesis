from email.mime import image
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

def main():
    dir_path = "/home/exjobb/code/master_thesis/image_processing"
    files = [
        "/test_color50x50.jpg",
        "/test_color100x100.jpg",
        "/test_color150x150.jpg",
        "/test_color200x200.jpg",
        "/test_color250x250.jpg",
        "/test_color300x300.jpg"
    ]

    
    #cv2.cvtColor(image_BGR, cv2.COLOR_BGR2GRAY)

    #gray = cv2.imread(dir_path + "/test500x500.jpg", cv2.IMREAD_COLOR)
    #sub1 = plt.subplot(4, 2, 1)
    #plt.imshow(gray)
    for file in files:
        gray = cv2.imread(dir_path + file, cv2.IMREAD_GRAYSCALE)

        plt.figure(file)
        resultimage = np.zeros((800, 800))
        for i in range(1, 6, 2):
            sobel_x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=i, scale=1)
            sobel_y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=i, scale=1)
            # sobel_x = cv2.normalize(cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=i), resultimage, 0, 1, cv2.NORM_MINMAX)
            # sobel_y = cv2.normalize(cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=i), resultimage, 0, 1, cv2.NORM_MINMAX)
            sub2 = plt.subplot(4, 2, i)
            plt.imshow(sobel_x, cmap="gray")
            sub3 = plt.subplot(4, 2, i+1)
            plt.imshow(sobel_y, cmap="gray")
        

            #sub1.title.set_text('Original')
            sub2.title.set_text(f'Sobel x with kernel size {i}')
            sub3.title.set_text(f'Sobel y with kernel size {i}')
        #plt.tight_layout()
        plt.subplots_adjust(
            top=0.965,
            bottom=0.0,
            left=0.13,
            right=0.9,
            hspace=0.225,
            wspace=0.14)
    plt.show()

    """
    top=0.965,
    bottom=0.0,
    left=0.13,
    right=0.9,
    hspace=0.225,
    wspace=0.14
    """
    

if __name__ == '__main__':
    main()
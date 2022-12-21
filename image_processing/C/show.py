import matplotlib.pyplot as plt
import numpy as np
import csv
import pathlib

def show_many(files: list):
    
    
    fig = plt.figure("image " + files[0][22])
    for i, file in enumerate(files):
        with open(str(pathlib.Path(__file__).parent.resolve()) + file) as csvfile:
            read = csv.reader(csvfile, delimiter=' ')

            buffer = list(read)
            for row in read:
                buffer.append(row)
        image = np.array(buffer, dtype=np.uint8)
        print(f"{file}:\nnbr pixels: {(np.sum(image) / 255)}, {(np.sum(image) / 255)/40000}%")
        image = np.reshape(image, (200, 200))
        fig.add_subplot(2, 3, i+1)
        plt.imshow(image, cmap="gray")
        plt.axis('off')
        plt.title(f"Test image {i+1}")
        plt.savefig()
    plt.show()
    
def show_one(file: str):
    
    plt.figure(file)
    with open(str(pathlib.Path(__file__).parent.resolve()) + file) as csvfile:
        read = csv.reader(csvfile, delimiter=' ')

        buffer = list(read)
        for row in read:
            buffer.append(row)
    image = np.array(buffer, dtype=np.uint8)
    print(f"{file}:\nnbr pixels: {(np.sum(image) / 255)}, {(np.sum(image) / 255)/40000}%")
    image = np.reshape(image, (200, 200))
    plt.imshow(image, cmap="gray")
    plt.show()

def main():
    things = ["sobel.csv", "threshold.csv", "diff_unfiltered.csv", "diff_filtered.csv"]
    files = [[f"/results_photoshopped/{i}/" + thing for i in range(2, 8, 1)] for thing in things]
    file = "/results_photoshopped/diff2.csv"
    #show_one(file)
    for row in files:
        show_many(row)

if __name__ == '__main__':
    main()
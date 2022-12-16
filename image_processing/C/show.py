import matplotlib.pyplot as plt
import numpy as np
import csv
import pathlib

def show_many(files: list):
    
    plt.figure("Many")
    for i, file in enumerate(files):
        with open(str(pathlib.Path(__file__).parent.resolve()) + file) as csvfile:
            read = csv.reader(csvfile, delimiter=' ')

            buffer = list(read)
            for row in read:
                buffer.append(row)
        image = np.array(buffer, dtype=np.uint8)
        print(f"{file}:\nnbr pixels: {(np.sum(image) / 255)}, {(np.sum(image) / 255)/40000}%")
        image = np.reshape(image, (200, 200))
        plt.subplot(2, 3, i+1)
        plt.imshow(image, cmap="gray")
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
    files = ["/test0.csv", "/test1.csv", "/RESULT1.csv", "/RESULT2.csv", "/RESULT.csv", "/RESULT_FILTERED.csv"]
    file = "/many_diffs/1.csv"
    show_one(file)
    #show_many(files)

if __name__ == '__main__':
    main()
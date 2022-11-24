import matplotlib.pyplot as plt
import numpy as np
import csv
import pathlib

def main():
    with open(str(pathlib.Path(__file__).parent.resolve()) + "/output.csv") as csvfile:
        read = csv.reader(csvfile, delimiter=' ')

        buffer = list(read)
        for row in read:
           buffer.append(row)
        #4: because of file overhead
    image = np.array(buffer, dtype=np.uint8)
    plt.imshow(image, cmap="gray")
    plt.show()

if __name__ == '__main__':
    main()
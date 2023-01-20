import matplotlib.pyplot as plt
import numpy as np
import pathlib
import csv

def load(file: str, inverted: bool = True) -> np.ndarray:
    
    folder = str(pathlib.Path(__file__).parent.resolve()) + "/"
    with open(folder + file) as csvfile:
        
        read = csv.reader(csvfile, delimiter=' ')
        buffer = list(read)
        for row in read:
            buffer.append(row)
        if inverted:
            buffer = [[abs(int(p)-255) for p in r] for r in buffer]
    image = np.array(buffer, dtype=np.uint8)
    
    return np.reshape(image, (200, 200))

def main():
    
    folder = str(pathlib.Path(__file__).parent.resolve())
    files = ["figures/reference.csv", "test0.csv", "test1.csv", "figures/sobeled.csv", "figures/thresholded.csv", "figures/diff_unfiltered.csv", "figures/diff_filtered.csv"]
    names = ["reference", "test image", "test image sobel", "test image threshold", "difference image", "filtered difference image"]

    #plt.subplots_adjust(left=0.293, bottom=0.014, right=0.77, top=0.955, wspace=0, hspace=0.09)
    #First figure
    plt.figure("Reference image and test image")
    plt.subplot(1, 2, 1)
    plt.imshow(load(files[1], False), cmap="gray")
    plt.axis('off')
    plt.title(names[0])
    plt.subplot(1, 2, 2)
    plt.imshow(load(files[2], False), cmap="gray")
    plt.title(names[1])
    plt.axis('off')
    plt.savefig(folder + "/figures/ref_test")
    
    plt.figure("Reference image processed")
    plt.imshow(load(files[0]), cmap="gray")
    plt.axis('off')
    plt.savefig(folder + "/figures/ref_proc")
    
    plt.figure("Processing of test image")
    plt.subplot(2, 2, 1)
    plt.imshow(load(files[2], False), cmap="gray")
    plt.title(names[1])
    plt.axis('off')
    plt.subplot(2, 2, 2)
    plt.imshow(load(files[3]), cmap="gray")
    plt.title(names[2])
    plt.axis('off')
    plt.subplot(2, 2, 3)
    plt.imshow(load(files[4]), cmap="gray")
    plt.title(names[3])
    plt.axis('off')
    plt.savefig(folder + "/figures/test_proc")
    
    plt.figure("Difference image")
    plt.subplot(1, 2, 1)
    plt.imshow(load(files[5]), cmap="gray")
    plt.title(names[4])
    plt.axis('off')    
    plt.subplot(1, 2, 2)
    plt.imshow(load(files[6]), cmap="gray")
    plt.title(names[5])
    plt.axis('off')
    plt.savefig(folder + "/figures/diff")

    plt.figure("Two reference images")
    plt.subplot(1, 2, 1)
    plt.imshow(load("many/ref1.csv", False), cmap="gray")
    plt.title("Reference 1")
    plt.axis('off')    
    plt.subplot(1, 2, 2)
    plt.imshow(load("many/ref2.csv", False), cmap="gray")
    plt.title("Reference 2")
    plt.axis('off')
    plt.savefig(folder + "/figures/diff")
    
    plt.show()

if __name__ == '__main__':
    main()
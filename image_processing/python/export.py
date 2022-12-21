import numpy as np
import pathlib
import cv2

def dump_csv(image: np.ndarray, filename: str) -> None:

    print(str(pathlib.Path(__file__).parent.resolve()) + filename)
    image.tofile(str(pathlib.Path(__file__).parent.resolve()) + filename, sep=' ', format='%d')
    
    
def main():
    
    here = str(pathlib.Path(__file__).parent.resolve()) + "/../C/Photoshopped/New_photoshopped"
    files =  [f"/{i}.jpg" for i in range(1, 8, 1)]
    images = np.array([cv2.cvtColor(cv2.imread(here + file), cv2.COLOR_BGR2GRAY) for file in files])
    
    dump_folder = "/../C/Photoshopped/New_photoshopped"
    for index, image in enumerate(images):
        file = f"/{index + 1}.csv"
        dump_csv(image, dump_folder + file)
    
if __name__ == '__main__':
    main()
    
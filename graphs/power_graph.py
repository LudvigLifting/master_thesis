import numpy as np
import matplotlib.pyplot as plt
import pathlib


#"Wall-clock time (UTC)","Arc Main Current (A)","Arc Main Voltage (V)","Arc Main Energy (J)"

if __name__ == '__main__':
    
    dir_path = str(pathlib.Path(__file__).parent.resolve())
    folder = "/test2.csv"
    file = dir_path + folder
    
    data = list()
    c = 0
    with open(file, 'r') as f:
        for line in f:
            line = line.rstrip()
            if c == 0:
                c += 1
                continue
            data.append(line.replace("\"", "").split(","))
    data = np.array(data)
    dt = 0.00025 #s
    #time = data[:,0]
    current = data[:, 1].astype(float)
    voltage = np.array([4.546 for _ in data[:, 2]])
    energy = data[:, 3].astype(float)
    
    plt.plot(current)
    plt.show()
    
    #remove things
    newcur = list()
    tmp = []
    for cur in current[50000:618000]:
        if cur > 0.0120:
            tmp.append(cur)
        else:
            if tmp:
                newcur.append(tmp)
                tmp = []
    print(len(newcur))
    #newcur = np.array(newcur)
    for i, send in enumerate(newcur):
        print(f"Peak {i} time = {dt*len(send)}s")
    
    
    
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    intensities = np.array([71, 82, 86, 89, 91, 93, 95, 96, 98, 100, 102, 103, 103, 106, 107, 108, 109, 110, 111, 112, 114, 115, 116, 117, 118, 121, 123, 124, 125, 127, 129, 129, 131, 131, 132, 132, 133, 135, 136, 137, 138, 139, 142, 143, 146, 147, 151, 178, 192])
    noise = np.array([1562, 1998, 2107, 1682, 2074, 1272, 1272, 2536, 2365, 1839, 1981, 2078, 2314, 1958, 2386, 2513, 2143, 1956, 2829, 1386, 2037, 1866, 2185, 1861, 2545, 1752, 1998, 2648, 2278, 1927, 2135, 1426, 1672, 2539, 2866, 2215, 1775, 2736, 2154, 2883, 2100, 2167, 1974, 2232, 1496, 2181, 1732, 2090, 1210])
    x = range(49)
    fit = np.polyfit(x, noise, 1, full=True)
    fit = np.poly1d(fit[0])
    
    plt.figure("Intensities and noise")
    plt.plot(x, intensities, label="intensities")
    plt.plot(x, noise, label="noise")
    plt.plot(x, fit(x), label="fitting noise")
    plt.legend()
    diff = (fit(x)-intensities)
    mean_diff = 0
    for dif in diff:
        mean_diff += dif
    mean_diff /= len(diff)
    plt.figure("Comparison")
    plt.plot(x, intensities+mean_diff, label="intensities")
    plt.plot(x, fit(x), label="offset noise")
    plt.legend()
    plt.show()
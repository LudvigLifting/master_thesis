import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    intensities = np.array([2, 4, 6, 7, 9, 10, 11, 13, 14, 14, 17, 18, 19, 19, 21, 23, 23, 23, 24, 25, 27, 28, 29, 29, 31, 32, 34, 34, 38, 39, 39, 42, 42, 43, 45, 47, 50, 52, 52, 57, 57, 58, 64, 67, 72, 98, 115, 131, 160])
    noise = np.array([1892, 2894, 2467, 2035, 2274, 2357, 2687, 2282, 1619, 2447, 1786, 2054, 1724, 1543, 2250, 2716, 1790, 2325, 1926, 2320, 2200, 2535, 2294, 2406, 2318, 1952, 2350, 2672, 2035, 3211, 2013, 2561, 2231, 2180, 2742, 2103, 2178, 1968, 3043, 1937, 2257, 2340, 2507, 2723, 2403, 3116, 2976, 3123, 3211])
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
    print(mean_diff)
    plt.figure("Comparison")
    plt.plot(x, intensities+mean_diff, label="intensities")
    plt.plot(x, fit(x), label="offset noise")
    plt.legend()
    plt.show()
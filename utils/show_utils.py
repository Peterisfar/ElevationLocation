import matplotlib.pylab as plt
import numpy as np


def show_dem_and_img(skyline_dem, ImageData):
    plt.figure(figsize=(96, 4.8))
    plt.plot(480 - np.array(skyline_dem))
    plt.xlim(0, 9600)
    plt.ylim(0, 480)

    plt.figure()
    plt.plot(480 - np.array(ImageData))
    plt.xlim(0, 640)
    plt.ylim(0, 480)
    plt.show()


def show_line_corner_and_tm(line, corner_q, t_M=None, size=(6.4,4.8)):
    corner_q_x, corner_q_y = zip(*corner_q)

    plt.figure(figsize=size)
    plt.plot(range(len(line)), 480 - np.array(line), color='green', label="query")
    plt.plot(corner_q_x, corner_q_y, "*", color="blue")

    if t_M:
        plt.plot(t_M, line[t_M], '^', color="red")

    plt.xlim(0,size[0]*100)
    plt.ylim(0,size[1]*100)
    plt.grid(True)
    plt.legend()
    plt.show()


def show_match_result_dem_and_img(S, T, Sc, Cost):
    print("******* resutlt is :*******")
    print("Sc : {} \nCost[Sc] : {}".format(Sc, Cost[Sc]))

    plt.figure()
    plt.plot([480 - x[1] for x in S[Sc]], label="Sc")
    plt.plot([480 - x[1] for x in T], label="T")
    plt.ylim(0, 480)
    plt.xlim(0, 640)
    plt.legend()
    plt.show()

    plt.figure()
    plt.plot(Cost, label="Cost")
    plt.legend()
    plt.show()



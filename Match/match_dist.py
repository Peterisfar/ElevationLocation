import math
import numpy as np


def get_gauss_kernel(r, sigma):
    kernelGauss = np.zeros(2 * r - 1)
    for i in range(2 * r - 1):
        kernelGauss[i] = math.exp(-(i - r) ** 2 / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))
    return kernelGauss

def distance_single(s, T):
    kernelGauss = get_gauss_kernel(3, 0.5)
    r = (len(kernelGauss) + 1) >> 1
    sy = [x[1] for x in s]
    s_y = np.convolve(sy, kernelGauss)[r - 1: -r + 1]
    st = [x[1] for x in T]
    s_t = np.convolve(st, kernelGauss)[r - 1: -r + 1]
    if len(s_y) < len(s_t):
        dict = np.sum(1.0*abs(s_t[:len(s_y)] - s_y) / len(s))
    elif len(s_y) > len(s_t):
        dict = np.sum(1.0 * abs(s_t - s_y[:len(s_t)]) / len(s))
    else:
        dict = np.sum(1.0 * abs(s_t - s_y) / len(s))
    return dict


def distance(S, T):
    dist = []
    for i in range(len(S)):
        dist.append(distance_single(S[i], T))
    Sc = dist.index(min(dist))
    return Sc, dist
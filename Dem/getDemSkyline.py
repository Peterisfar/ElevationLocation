import cv2
import os
import numpy as np
import csv
import copy
import math


def get_gauss_kernel(r, sigma):
    kernelGauss = np.zeros(2 * r - 1)
    for i in range(2 * r - 1):
        kernelGauss[i] = math.exp(-(i - r) ** 2 / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))
    return kernelGauss


def GaussLineBlur(line):
    kernelGauss = get_gauss_kernel(3, 0.5)
    r = (len(kernelGauss) + 1) >> 1
    line_new = np.convolve(line, kernelGauss)[r - 1: -r + 1]
    return list(map(int, line_new))


def mean_filter(arr, step):
    """
    平滑滤波函数，输入是一个列表，输出是这个列表平滑之后的值。即取step个数的平均值
    :param arr:列表
    :param step:以多大步长取平均
    :return:平滑后的列表
    """
    new_arr = arr[:int(step / 2)]
    for kk in range(int(step / 2), len(arr) - step + int(step / 2)):
        new_arr.append(int(sum(arr[kk - int(step / 2):kk + step - int(step / 2)]) / step))
    new_arr.extend(arr[-(step - int(step / 2)):])
    return new_arr


def show_line_on_img(img, line):
    """img : original img(3channels, numpy)
       line : skyline from DEM (list)"""
    points = list(zip(range(len(line)), line))
    for i, pt in enumerate(points):
        if i == len(points) - 1:
            break
        cv2.line(img, points[i], points[i + 1], (0, 0, 255), 1)
    cv2.imshow("img", img)

    cv2.waitKey(0)

def img2line(ori):
    """
    ori : origin img
    img : img : ori_R channel (numpy)
    """
    img = copy.deepcopy(ori)
    h, w, _ = img.shape
    img_mean = np.mean(img[..., 1:], axis=-1)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_s = img_hsv[..., 1]
    line = []
    for wi in range(w):
        img_s_col = img_s[:, wi]
        img_GR_col = img_mean[:, wi]
        for hi, pixl in enumerate(img_s_col):
            # way1---> not good
            if (pixl != np.array([240, 149, 137])).all():
                line.append(hi)  # height need to adjust(opencv)
                break

            # way2---> threshold
            # if img_GR_col[hi] >144 or img_GR_col[hi] < 140:
            #     if pixl < 100 or pixl > 200:
            #         line.append(hi)
            #         break

            # way3---> linear point threshold --->not good
            # dist = np.sum(np.abs(pixl-img_col[hi+1]))
            # if dist > 10:
            #     line.append(hi)
            #     break

    # filter line
    line = mean_filter(line, 3)
    show_line_on_img(ori, line)
    return line

def getDemSkylinesCsv(imgs_dir, csv_path):
    filenames = os.listdir(imgs_dir)

    for i, filename in enumerate(filenames):
        img_path = os.path.join(imgs_dir, filename)
        print(i, img_path)
        img = cv2.imread(img_path)
        # cv2.imshow("img", img)
        # cv2.waitKey(0)

        line = img2line(img)

        # save line to csv
        with open(csv_path, 'a', newline='') as f:
            f_csv = csv.writer(f)
            line.insert(0, filename)
            f_csv.writerow(line)



if __name__ == "__main__":
    """need : panorams DEM pictures
              csv save path
       return : csv file
    """
    imgs_dir = "../data/panoramas"
    csv_path = "../data/result.csv"

    if os.path.isfile(csv_path):
        os.remove(csv_path)

    getDemSkylinesCsv(imgs_dir, csv_path)

    print('Done!')
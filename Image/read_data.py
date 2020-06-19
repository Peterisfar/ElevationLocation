from gps_data_solve import gps_data_solve
import numpy as np
import cv2
import matplotlib.pylab as plt


def mask2line(img):
    height, width, _ = img.shape
    line = []
    for w in range(width):
        for h in range(height):
            if (img[h,w] == np.array([0, 0, 255])).all():
                line.append(h)
                break
    # 如果line的长度少于640则默认少的部分填补line[0]
    if len(line)<640:
        line = [line[0]]*(640-len(line)) + line
    return line


def read_data_to_txt(path):
    print("******* test image info is :********")
    # show lon and lat
    gps_data_solve(path.replace('_res',''))

    # get skyline
    points = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            points.append(tuple(map(int, line.split(','))))

    img = np.zeros((480, 640, 3), np.uint8)
    for i, point in enumerate(points):
        if i == len(points) -1:
            break
        cv2.line(img, points[i], points[i+1], (0,0,255), 1)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)

    skyline = mask2line(img)  # list

    return skyline


if __name__ == '__main__':
    line = read_data_to_txt("../data/09_59_19_res.txt")
    plt.plot(480 - np.array(line))
    plt.xlim(0,640)
    plt.ylim(0,480)
    plt.show()
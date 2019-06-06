#coding=utf-8
import icp
import numpy as np
import matplotlib.pyplot as plt
import cv2


def rotation_matrix():
    a = 0.5
    while a < 0.7:
        a = np.random.random()
    b = np.sqrt(1 - a ** 2)
    return np.array([[a,-b],[b,a]])


def linePoints(image, points, size=1,color=(255,255,255)):
    for i in range(points.shape[0]-1):
        p1 = points[i]
        p2 = points[i+1]
        cv2.line(image, (int(p1[0]),int(p1[1])), (int(p2[0]),int(p2[1])), color, size)


def single_line_fit(skyline_r, skyline_q):
    dim = 2  # number of dimensions of the points
    noise_sigma = 10  # standard deviation error to be added
    translation = 100  # max translation of the test set
    rotation = .1  # max rotation (radians) of the test set
    # image_base = np.zeros((4800, 640, 3), dtype=np.uint8)

    new_points = np.array(list(zip(range(len(skyline_q)), skyline_q)), dtype=np.float32)
    t = np.random.rand(dim) * translation
    R = rotation_matrix()
    new_points += t
    new_points = np.dot(R, new_points.T).T
    # linePoints(image_base, new_points, size=2, color=(0, 0, 255))

    skyline = skyline_r
    length = len(skyline)
    ref_points = np.array(list(zip(range(length), skyline)), dtype=np.float32)
    # linePoints(image_base, ref_points, size=2, color=(0, 255, 0))

    # cv2.imshow('image', image_base)
    # cv2.waitKey(0)

    fit_points = np.copy(new_points)
    for i in range(10):
        # image = np.copy(image_base)
        r, t, err, indices = icp.icp(fit_points, ref_points, max_iterations=1, tolerance=0.8, index=True)
        # for p1, p2 in zip(fit_points, ref_points[indices]):
        #     cv2.line(image, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (0, 0, 255), 1)
        #     cv2.circle(image, (int(p1[0]), int(p1[1])), 1, (255, 0, 255), 1)
        # linePoints(image, fit_points, size=2, color=(255, 0, 255))
        fit_points = np.dot(r, fit_points.T).T + t

        # cv2.putText(image, 'err = {}'.format(err), (20, 30), 2, cv2.FONT_HERSHEY_PLAIN, (255, 0, 0))
        # cv2.imshow('image', image)
        # cv2.waitKey(max(int(err) * 5, 10))
        if err < 0.8:
            break
        # print 'r = {}\nt = {}\nmean_err = {}'.format(r, t, err)
    # print 'Done.'
    # cv2.imshow('image', image)
    # cv2.waitKey(0)
    return err


def distance(S, T):
    """calculate the dist between S and T"""
    ss = [[x[1] for x in S[i]] for i in range(len(S))]  # S_y
    t = [x[1] for x in T]  # T_y
    errs = []
    for s in ss:
        errs.append(single_line_fit(s, t))
    best_p = errs.index(min(errs))
    return best_p, errs
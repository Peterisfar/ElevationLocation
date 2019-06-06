import math
import copy
from functools import reduce


def polar_to_rectangular(line):
    r_min = 0
    y = [(line[1][i]-r_min) * math.cos(line[0][i]) for i in range(len(line[0]))]
    x = [(line[1][i]-r_min) * math.sin(line[0][i]) for i in range(len(line[0]))]
    return x, y


def diffusion_function(s):
    rho = 0.2
    return math.exp(-(1.0 * s / rho) ** 2)


def anisotropic_filter(B):
    step = 0.2  # step size
    iter_num = 1000 # the number of iterations
    B_tmp = copy.deepcopy(B)
    for n in range(iter_num):
        for i in range(len(B)):
            if n == 0 :
                B_tmp[i] = B[i]
            else:
                if i>0 and i<(len(B)-1):
                    b_p = B[i+1] - B[i]
                    b_m = B[i-1] - B[i]
                    B_tmp[i] += 1.0*step*(diffusion_function(b_p)*b_p + diffusion_function((b_m)*b_m))
                elif i == 0 :
                    b_p = B[i + 1] - B[i]
                    b_m = B[i - 1] - B[i]
                    B_tmp[i] += 1.0 * step * (diffusion_function(b_p) * b_p + diffusion_function((b_m) * b_m))
                elif i >= (len(B)-1):
                    b_p = B[i + 1 - len(B)] - B[i]
                    b_m = B[i - 1] - B[i]
                    B_tmp[i] += 1.0 * step * (diffusion_function(b_p) * b_p + diffusion_function((b_m) * b_m))
        B = copy.deepcopy(B_tmp)
    return B


def corner_detection(line):
    X = line[0]
    Y = line[1]
    l = len(X)
    # first step : calculate curvature value
    K = 1
    P_curvature = []
    for i in range(l):
        if i<K:
            alpha = X[i + K] - X[i - K]
            epsilon = Y[i + K] - 2 * Y[i] + Y[i - K]
            gamma = Y[i + K] - Y[i - K]
            delta = X[i + K] - 2 * X[i] + X[i - K]
        elif i > (l - K - 1):
            alpha = X[i + K - l] - X[i - K]
            epsilon = Y[i + K - l] - 2 * Y[i] + Y[i - K]
            gamma = Y[i + K - l] - Y[i - K]
            delta = X[i + K - l] - 2 * X[i] + X[i - K]
        else:
            if i == 314:
                pass
            alpha = X[i+K] - X[i-K]
            epsilon = Y[i+K] - 2*Y[i] + Y[i-K]
            gamma = Y[i+K] - Y[i-K]
            delta = X[i+K] - 2*X[i] + X[i-K]
        if alpha != 0 and gamma !=0:
            psi = (1.0 * alpha * epsilon - 1.0 * gamma * delta) / ((alpha)**2 + (1.0 * gamma)**2)**(3.0/2)
        else:
            psi = (1.0 * alpha * epsilon - 1.0 * gamma * delta) / 0.001 **(3.0/2)
        # psi = (1.0 * alpha * epsilon - 1.0 * gamma * delta) / ((alpha) ** 2 + (1.0 * gamma) ** 2) ** (3.0 / 2)
        P_curvature.append(psi)

    # second step : anisotropic filter
    P_curvature_new = anisotropic_filter(P_curvature)

    # third step : localizing the corner points
    P_corner = []
    P_conner_index = []
    for i in range(len(P_curvature_new)):
        if i>0 and i<(len(P_curvature_new)-1):
            if P_curvature_new[i]>0:
                if (P_curvature_new[i]-P_curvature_new[i-1])>0:
                    if (P_curvature_new[i]-P_curvature_new[i+1])>0:
                        P_corner.append(P_curvature_new[i])
                        P_conner_index.append(i)
            if P_curvature_new[i]<0:
                if (P_curvature_new[i]-P_curvature_new[i-1])<0:
                    if (P_curvature_new[i]-P_curvature_new[i+1])<0:
                        P_corner.append(P_curvature_new[i])
                        P_conner_index.append(i)
        elif i == 0 :
            if P_curvature_new[i]>0:
                if (P_curvature_new[i]-P_curvature_new[i-1])>0:
                    if (P_curvature_new[i]-P_curvature_new[i+1])>0:
                        P_corner.append(P_curvature_new[i])
                        P_conner_index.append(i)
            if P_curvature_new[i]<0:
                if (P_curvature_new[i]-P_curvature_new[i-1])<0:
                    if (P_curvature_new[i]-P_curvature_new[i+1])<0:
                        P_corner.append(P_curvature_new[i])
                        P_conner_index.append(i)
        elif i >= (len(P_curvature_new)-1):
            if P_curvature_new[i]>0:
                if (P_curvature_new[i]-P_curvature_new[i-1])>0:
                    if (P_curvature_new[i]-P_curvature_new[i+1-len(P_curvature_new)])>0:
                        P_corner.append(P_curvature_new[i])
                        P_conner_index.append(i)
            if P_curvature_new[i]<0:
                if (P_curvature_new[i]-P_curvature_new[i-1])<0:
                    if (P_curvature_new[i]-P_curvature_new[i+1-len(P_curvature_new)])<0:
                        P_corner.append(P_curvature_new[i])
                        P_conner_index.append(i)
    return P_conner_index, P_corner, P_curvature


def select_informative_corner(Q, P_curve):
    I_Q = []
    for i in range(len(Q)):
        I_p = reduce(lambda x,y: x + y , map(abs, P_curve[Q[i]:]))
        I_m = reduce(lambda x,y: x + y , map(abs, P_curve[:(Q[i]+1)]))
        I_Q.append(min(I_p, I_m))

    I_Q_M = max(I_Q)
    t_M = Q[I_Q.index(I_Q_M)]
    return t_M, I_Q_M


def pretreat_q(skyline_q):
    """输入skyline_q, 得到tm 和 portion, shape, curve, corner"""
    corner_index_q, _, p_c_q = corner_detection([range(len(skyline_q)), skyline_q])
    corner_q_x = corner_index_q
    corner_q_y = [skyline_q[i] for i in corner_index_q]
    t_M, I_Q = select_informative_corner(corner_index_q, p_c_q)
    X_q = range(len(skyline_q))
    Y_q = skyline_q
    portion = [t_M, len(X_q) - t_M]
    shape_q = list(zip(X_q, Y_q))
    curve_q = p_c_q
    corner_q = list(zip(corner_q_x, corner_q_y))
    tm = [t_M, Y_q[t_M]]
    return portion, shape_q, curve_q, corner_q, tm


def pretreat_d(skyline_d):
    corner_index_d, _, p_c_d = corner_detection([range(len(skyline_d)), skyline_d])
    corner_d_x = corner_index_d
    corner_d_y = [skyline_d[j] for j in corner_index_d]
    X_d = range(len(skyline_d))
    Y_d = skyline_d
    shape_d = list(zip(X_d, Y_d))
    curve_d = p_c_d
    corner_d = list(zip(corner_d_x, corner_d_y))

    return shape_d, curve_d, corner_d
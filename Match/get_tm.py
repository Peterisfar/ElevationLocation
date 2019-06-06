


def pretreat_q(skyline_q):
    corner_index_q, _, p_c_q = corner_detection.corner_detection([range(len(skyline_q)), skyline_q])
    corner_q_x = corner_index_q
    corner_q_y = [skyline_q[i] for i in corner_index_q]
    t_M, I_Q = corner_detection.select_informative_corner(corner_index_q, p_c_q)
    X_q = range(len(skyline_q))
    Y_q = skyline_q
    portion = [t_M, len(X_q) - t_M]
    shape_q = map(lambda x, y: [x, y], X_q, Y_q)
    curve_q = p_c_q
    corner_q = map(lambda x, y: [x, y], corner_q_x, corner_q_y)
    tm = [t_M, Y_q[t_M]]
    return index_q, q_left_index, portion, shape_q, curve_q, corner_q, tm
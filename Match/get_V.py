def get_Vmaxtix_one(shape, curve, corners, t):
    V = shape
    c = curve
    return V, c, t


def get_Vmaxtix(shape, curve, corners, tm=None, portion=None):
    if tm != None:
        V, C, t= get_Vmaxtix_one(shape, curve, corners, tm)
        return V, C, t
    V = []
    C = []
    T = []
    for corner in corners:
        index = shape.index(corner)
        left = index-portion[0]
        right = index+portion[1]

        if left<0:
            shape_part = shape[left:] + shape[:right]
            curve_part = curve[left:] + curve[:right]
        elif right>len(shape):
            shape_part = shape[left:] + shape[:right-len(shape)]
            curve_part = curve[left:] + curve[:right-len(shape)]
        else:
            shape_part = shape[left:right]
            curve_part = curve[left:right]

        corners_part = []
        for corner_tmp in corners:
            if corner_tmp in shape_part:
                corners_part.append(corner_tmp)

        V_part, C_part, t_part = get_Vmaxtix_one(shape_part, curve_part, corners_part, corner)
        V.append(V_part)
        C.append(C_part)
        T.append(t_part)
    return V, C, T
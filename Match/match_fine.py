




def get_close_S(shape, sc, portion, k):
    S = []
    yaws = []
    sc = int(sc)
    for i in range(-k, k+1):
        left = sc + i - portion[0]
        right = sc + i + portion[1]

        if left<0 and right >0:
            shape_part = shape[left:] + shape[:right]
        elif left<0 and right <=0:
            shape_part = shape[len(shape) + left:len(shape)+right]
        elif right>len(shape):
            shape_part = shape[left:] + shape[:right-len(shape)]
        else:
            shape_part = shape[left:right]

        S.append(shape_part)
        yaws.append((left+right)//2)
    return S, yaws
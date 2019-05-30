import read_datas
import corner_detection


def write_database(path_dem):
    skylines_d = read_datas.read_data(path_dem)[0:1000]
    for i in range(len(skylines_d)):
        print (i)
        skyline_d = skylines_d[i]

        corner_index_d, _, p_c_d = corner_detection.corner_detection([range(len(skyline_d)), skyline_d])
        corner_d_x = corner_index_d
        corner_d_y = [skyline_d[j] for j in corner_index_d]
        X_d = range(len(skyline_d))
        Y_d = skyline_d
        shape_d = map(lambda x, y: [x, y], X_d, Y_d)
        curve_d = p_c_d
        corner_d = map(lambda x, y: [x, y], corner_d_x, corner_d_y)

        f = open("./data/1000.txt", 'a')
        f.writelines([str(shape_d),";",str(curve_d),';',str(corner_d),'\n'])
    f.close()


def read_database(lines, i):
    s1 = lines[i].strip().split(';')[0]
    s2 = lines[i].strip().split(';')[1]
    s3 = lines[i].strip().split(';')[2]

    s1_s = s1.strip().split(',')
    shape_d = []
    for i, p in enumerate(s1_s):
        if i % 2 == 0:
            shape_d.append([int(s1_s[i]), float(s1_s[i + 1])])

    s2_s = s2.strip().split(',')
    curve_d = map(float, s2_s)

    s3_s = s3.strip().split(',')
    corner_d = []
    for i, p in enumerate(s3_s):
        if i % 2 == 0:
            corner_d.append([float(s3_s[i]), float(s3_s[i + 1])])

    return shape_d, curve_d, corner_d


if __name__ == "__main__":
    write_database(path_dem = "./data/data_geo3k/dem.txt")
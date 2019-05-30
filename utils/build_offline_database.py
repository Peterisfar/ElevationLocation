from Match.corner_detection import *
from Match.get_V import *

import csv
import json

from Image.read_data import *


# step 1 : prepare datas
DemDatas = csv.reader(open("../data/result.csv", 'r'))  # 360 ---> 9600
ImageData = read_data_to_txt("../data/09_59_19_res.txt")  # 24 --->640  (list)

# step 2 : produce image data , get tm
portion, shape_q, curve_q, corner_q, tm = pretreat_q(ImageData)

database = []

for i, skyline_dem in enumerate(DemDatas):
    print(i)
    data = {}
    skyline_dem = list(map(int, skyline_dem[1:]))
    shape_d, curve_d, corner_d = pretreat_d(skyline_dem)
    # step 3 : 得到形状片段集
    S, S_curve, S_corner = get_Vmaxtix(shape_d, curve_d, corner_d, portion=portion)

    data["filename"] = skyline_dem[0]
    data["S"] = S
    data["S_curve"] = S_curve
    data["S_corner"] = S_corner
    data["shape_d"] = shape_d
    data["curve_d"] = curve_d
    data["corner_d"] = corner_d

    database.append(data)

with open("../data/result.json", 'w') as f:
    json.dump(database, f)
    print("保存json文件完成....")
from Match.corner_detection import *
from Match.get_V import *

import csv
import pandas as pd

from Image.read_data import *
from utils.show_utils import *

# from Match.match_icp import *
from Match.match_fine import *
from Match.nnnet.match_net import *
from Match.nnnet import model as mm
import torch

Cost_all = []

device = torch.device("cpu")

model = mm.SiameseNetwork()
model.load_state_dict(torch.load("./data/checkpoint//2019-05-23_best.pth", map_location='cpu'))
model.to(device)

# step 1 : prepare datas
DemDatas = csv.reader(open("./data/result.csv", 'r'))  # 360 ---> 9600
ImageData = read_data_to_txt("./data/09_59_19_res.txt")  # 24 --->640  (list)


# step 2 : produce image data , get tm
portion, shape_q, curve_q, corner_q, tm = pretreat_q(ImageData)
# show_line_corner_and_tm(ImageData, corner_q, tm[0])


for i, skyline_dem in enumerate(DemDatas):

    skyline_dem = list(map(int, skyline_dem[1:]))
    if i == 4210:
        print(skyline_dem[0])
        skyline_dem = list(map(int, skyline_dem[1:]))
        show_dem_and_img(skyline_dem, ImageData)

        shape_d, curve_d, corner_d = pretreat_d(skyline_dem)
        # show_line_corner_and_tm(skyline_dem, corner_d, size=(96, 4.8))

        # step 3 : 得到形状片段集
        S, S_curve, S_corner = get_Vmaxtix(shape_d, curve_d, corner_d, portion=portion)
        T, T_curve, T_corner = get_Vmaxtix(shape_q, curve_q, corner_q, tm=tm)

        # step 4 : 计算代价
        Sc, Cost = distance(S, T, model)
        # show_match_result_dem_and_img(S, T, Sc, Cost)

        # step 5 : 精调
        corner_d_x, corner_d_y = zip(*corner_d)
        S = get_close_S(shape_d, corner_d_x[Sc], portion, 20)
        Sc, Cost = distance(S, T, model)
        show_match_result_dem_and_img(S, T, Sc, Cost)

        # step 6 : 保存结果
        print(i, Cost[Sc])
        Cost_all.append(Cost[Sc])

df = pd.Series(Cost_all).sort_values()
print(df)
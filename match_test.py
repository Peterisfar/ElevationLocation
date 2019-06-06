from Match.corner_detection import *
from Match.get_V import *

import csv
import pandas as pd
import os
import json
import time

from Image.read_data import *
from utils.show_utils import *
from utils.tools import *

# from Match.match_icp import *
from Match.match_fine import *
from Match.nnnet.match_net import *
from Match.nnnet import model as mm
import torch

Cost_all = []
latitude_all = []
longitude_all = []
yaw_all = []


device = torch.device("cuda:0")

model = mm.SiameseNetwork()
model.load_state_dict(torch.load("./data/locdata/checkpoint//2019-05-23_best.pth", map_location=device))
model.to(device)

# step 1 : prepare datas
ImageData = read_data_to_txt("./data/locdata/test/10_32_38_res.txt")  # 24 --->640  (list)
Demfilenames = os.listdir("./data/locdata/result")


# step 2 : produce image data , get tm
portion, shape_q, curve_q, corner_q, tm = pretreat_q(ImageData)
T, T_curve, T_corner = get_Vmaxtix(shape_q, curve_q, corner_q, tm=tm)
# show_line_corner_and_tm(ImageData, corner_q, tm[0])


for i, skyline_dem in enumerate(Demfilenames):
    # if i == 4210:
    with open(os.path.join("./data/locdata/result", skyline_dem)) as f:
        Demdata = json.load(f)
    filename = Demdata["filename"]

    shape_d = Demdata["shape_d"]
    curve_d = Demdata["curve_d"]
    corner_d = Demdata["corner_d"]

    # step 3 : 得到形状片段集
    S = Demdata["S"]
    S_curve = Demdata["S_curve"]
    S_corner = Demdata["shape_d"]

    # step 4 : 计算代价
    time1 = time.time()
    Sc, _ = distance(S, T, model, device)
    # show_match_result_dem_and_img(S, T, Sc, Cost)
    print(time.time()-time1)

    # step 5 : 精调
    time1 = time.time()
    corner_d_x, corner_d_y = zip(*corner_d)
    S, yaws = get_close_S(shape_d, corner_d_x[Sc], portion, 50)
    Sc, Cost = distance(S, T, model, device)
    # show_match_result_dem_and_img(S, T, Sc, Cost)
    print(time.time()-time1)

    # step 6 : 保存结果
    print(i, filename, Cost[Sc])
    lon, lag = list(map(float, filename[:-4].split('-')))
    yaw = get_yaw_angle(yaws[Sc])
    print("yaw : {}°".format(yaw))
    longitude_all.append(lon)
    latitude_all.append(lag)
    Cost_all.append(Cost[Sc])
    yaw_all.append(yaw)

df = pd.DataFrame({'lon':longitude_all, 'lat':latitude_all, 'yaw':yaw_all, 'score':Cost_all}).sort_values(by='score', ascending=False)
# print(df)
df.to_csv("./data/locdata/match_result_3.csv")
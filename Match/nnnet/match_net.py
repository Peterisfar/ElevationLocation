from __future__ import print_function
import os
import random
from tqdm import trange
import torch
import torch.nn.parallel
from torch.autograd import Variable
import json
import pandas as pd
import numpy as np


import nnnet.model as mm
from nnnet.tools import *


def distance_single(net, line0, line1, device="cpu"):
    net.eval()

    with torch.no_grad():
        length = len(line1)
        line = np.hstack((line0, line1))
        line_min, line_max = line.min(), line.max()
        line = (line - line_min) / (line_max - line_min)
        line1 = torch.from_numpy(line[:length].reshape(1, 1, -1))
        line2 = torch.from_numpy(line[length:].reshape(1, 1, -1))

        output = net(line1.float().to(device), line2.float().to(device))

        return torch.sigmoid(output)[0][1].item()

def distance(S, T, model):

    ss = [[x[1] for x in S[i]] for i in range(len(S))]  # S_y
    t = [x[1] for x in T]  # T_y
    errs = []
    for s in ss:
        errs.append(distance_single(model, [s[i] for i in range(0,640,2)], [t[i] for i in range(0,640,2)]))
    best_p = errs.index(max(errs))
    return best_p, errs


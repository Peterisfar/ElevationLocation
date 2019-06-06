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
import time


import nnnet.model as mm
from nnnet.tools import *


def distance_single(net, line0, line1, device="cpu"):
    net.eval()

    with torch.no_grad():
        batch, length = line0.shape
        line = np.hstack((line0, line1))
        line_min, line_max = line.min(axis=1), line.max(axis=1)
        line = (line - line_min.reshape(-1, 1)) / (line_max - line_min).reshape(-1,1)
        line1 = torch.from_numpy(line[:, :length].reshape(batch, 1, -1))
        line2 = torch.from_numpy(line[:, length:].reshape(batch, 1, -1))

        output = net(line1.float().to(device), line2.float().to(device))

        return torch.sigmoid(output)[:, 1].cpu().numpy()


def distance(S, T, model, device="cpu"):
    num = len(S)
    ss = np.array([[x[1] for x in S[i]][::2] for i in range(len(S))])  # S_y
    t = np.array([[x[1] for x in T][::2]]).repeat((num, ), axis=0)  # T_y

    errs = distance_single(model, ss, t, device)
    best_p = errs.argmax()

    return best_p, errs

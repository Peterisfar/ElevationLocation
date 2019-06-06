import matplotlib.pylab as plt
import csv
import numpy as np
import math
from utils.tools import *


csv_file = csv.reader(open("./data/locdata/match_result.csv", 'r'))

x0 = 112.808
y0 = 28.1604
yaw0 = 222
# x0 = 112.76108
# y0 = 28.1493
# yaw0 = 356.36
# x0 = 112.7559
# y0 = 28.1526
# x0 = 112.7611
# y0 = 28.1493


X = np.arange(112.69000, 112.83000, 0.002)
Y = np.arange(28.08000, 28.22000, 0.002)
X, Y = np.meshgrid(X, Y)

Z = np.zeros((len(X[0]),len(Y[0])))

for i, data in enumerate(csv_file):
    if i == 0:
        continue
    lat, lon, yaw, score= list(map(float, data[1:]))
    if score > 0.8 and get_yaw_in_area(yaw, yaw0, 50):
        row = int((lon - 112.6900) / 0.002)
        col = int((lat - 28.08000) / 0.002)
        Z[col, row] = score  # numpy存储方向相反

        length = math.sqrt((lon-x0)**2 + (lat-y0)**2) / 0.002 * 200
        print(lat, lon, score, length)

# Z = np.clip(Z,0.7,1)
plt.contourf(X, Y, Z, 8)
plt.colorbar(shrink=.83)

plt.scatter([x0,],[y0],s = 20, color='b')
plt.show()
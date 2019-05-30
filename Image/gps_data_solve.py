#coding=utf-8


def gps_data_translate(a):
    """将gps设备数据转化为度分秒形式，和十进制形式"""
    degree = int(a) // 100
    minute = int(a) % 100
    second = (a - int(a)) * 60

    decimal = degree + minute/60.0 + second/3600.0

    return degree, minute, second, decimal



def read_gpsdata_txt(path):
   with open(path, 'r') as f:
       lines = f.readlines()
       latitude = float(lines[3].split(':')[-1])
       longitude = float(lines[4].split(':')[-1])

   return latitude, longitude


def gps_data_solve(path):
    latitue, longitude = read_gpsdata_txt(path)
    # print latitue, longitude
    degree_lat,  minute_lat, second_lat, decimal_lat = gps_data_translate(latitue)
    degree_lon,  minute_lon, second_lon, decimal_lon = gps_data_translate(longitude)

    print ("latitude  N%d°%d′%.2f″" %(degree_lat,  minute_lat, second_lat))
    print ("longitude  E%d°%d′%.2f″" %(degree_lon,  minute_lon, second_lon))

    print("latitude : {}".format(decimal_lat) + "\n" + "longitude : {}".format(decimal_lon))
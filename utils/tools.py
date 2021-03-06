

def get_yaw_angle(x):
    if x < 0:
        x = x + 9600
    if x >= 9600:
        x = x - 9600

    if x < 7200:
        yaw = (360.0 / 9600) * x + 45
    else:
        yaw = (x - 7200) * (360.0 / 9600) + 0

    return yaw


def get_yaw_in_area(yaw, yaw0, area=30):
    if yaw>area and yaw<360-area:
        if abs(yaw0 - yaw) < area:
            return True
        else:
            return False
    elif yaw<area:
        if yaw > 360-area+yaw0 or yaw < yaw0+area:
            return True
        else:
            return False
    else:
        if yaw < area-360+yaw0 or yaw > yaw0 - area:
            return True
        else:
            return False
import numpy as np
def orientation(c1,c2,c3,c4):
    point1=(c1+c2)/2
    point2=(c3+c4)/2
    dif=point2-point1
    orient=np.degrees(np.arctan2(dif[1],dif[0]))
    return orient

import numpy as np
from aStar import Map
import matplotlib.pyplot as plt
import time
from camera import MobileCamera

MAP = np.zeros((500, 500))
MAP_T = np.zeros((500, 500))
MAP[0, :] = 100
MAP[499, :] = 100
MAP[:, 0] = 100
MAP[:, 499] = 100
MAP_T[:, :] = np.inf

cam = MobileCamera("http://192.168.0.119:1111/video")
markers,image=cam.getImage()
while not (4 in markers and 5 in markers):
    markers,image=cam.getImage()

bots=[]
for i in markers:
    bots.append(*markers[i],i)

x_init=bots[0].pos
x_final=bots[1].pos

m=Map(500, 500, MAP, x_init, x_final, MAP_T)
path, t = m.getPath()

plt.imshow(image)
plt.plot(path[:,0],path[:,1])
plt.xlim(0,500)
plt.ylim(0,500)
plt.show()

import numpy as np
from aStar import Map
import matplotlib.pyplot as plt
import time
from camera import MobileCamera
from bots import Bot

camera = MobileCamera("http://192.168.0.119:1111/video")

MAP = np.zeros((500, 500))
MAP_T = np.zeros((500, 500))
MAP[0, :] = 100
MAP[499, :] = 100
MAP[:, 0] = 100
MAP[:, 499] = 100
MAP_T[:, :] = np.inf

botIDs = [4, 5]
bots = []
for id in botIDs:
    bots.append(Bot(id))

x_init = bots[0].pos
x_final = bots[1].pos

m = Map(500, 500, MAP, x_init, x_final, MAP_T)
path, t = m.getPath()

plt.imshow(camera.getEnvironment())
plt.plot(path[:, 0], path[:, 1])
plt.xlim(0, 500)
plt.ylim(0, 500)
plt.show()

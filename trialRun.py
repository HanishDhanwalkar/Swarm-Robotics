import numpy as np
from aStar import Map
import matplotlib.pyplot as plt
import time
from camera import MobileCamera
from bots import Bot,Box
from control import control

camera = MobileCamera("http://192.168.0.101:1111/video")

MAP = np.zeros((500, 500))
MAP_T = np.zeros((500, 500))
MAP[0, :] = 100
MAP[499, :] = 100
MAP[:, 0] = 100
MAP[:, 499] = 100
MAP_T[:, :] = np.inf
Kp_r = 0.1
Kp_theta = 0.1
Kd_r = 0.1
Kd_theta = 0.1

botIDs = [4,6,8]
bots = []
for id in botIDs:
    bots.append(Bot(id))

boxIDs = [5,7,9]
dest=np.random.randint(30, 80, (4, 2))
boxs = []
for id in boxIDs:
    boxs.append(Box(id))

for i in range(len(boxs)):
    boxs[i].dest=dest[i]
    bots[i].assignBox(boxs[i])
    
p=[]
t=[]
tb=[]

for i in range(len(bots)):
    print(i)
    p1, t1, tb1 = bots[i].createPath(MAP, MAP_T)
    p.append(p1)
    # print(MAP[list(map(list, p[i].T))[0],list(map(list, p[i].T))[1]])
    t.append(t1)
    tb.append(tb1)

    MAP[list(map(list, p[i].T))[0],list(map(list, p[i].T))[1]] = 100
    #print(MAP_T[p[i]],t[i].shape)
    MAP_T[list(map(list, p[i].T))[0],list(map(list, p[i].T))[1]] = t[i]
    MAP_T[p[i][-1][0], p[i][-1][1]] = np.inf

plt.imshow(camera.getEnvironment())
for i in range(len(bots)):
    plt.plot(p[i][:, 0], p[i][:, 1])
plt.xlim(0, 500)
plt.ylim(0, 500)
plt.show()

tic = time.time()
while True:
    for bot in bots:
        toc = time.time()
        t = toc - tic
        bot.updatePos()
        exp_pos = bot.position(t)
        dr = bot.distFromPoint(exp_pos)
        dtheta = bot.orientation(t) - bot.theta
        V = Kp_r*dr + Kd_r*bot.speed
        Vleft = int(V - Kp_theta*dtheta - Kd_theta*bot.omega)
        Vright = int(V + Kp_theta*dtheta + Kd_theta*bot.omega)
        if Vleft > 255:
            Vleft = 255
        if Vleft < -255:
            Vleft = -255
        if Vright > 255:
            Vright = 255
        if Vright < -255:
            Vright = -255
        control(bot.id,Vright,Vleft)
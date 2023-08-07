import numpy as np
from aStar import Map
import matplotlib.pyplot as plt
import time
from camera import MobileCamera
from bots import Bot,Box
from control import control
import requests
from server import StartServer

print('Start')
camera = MobileCamera("http://192.168.122.86:1111/video",debug =False)
print('Cam Connected.')

MAP = np.zeros((610, 460))
MAP_T = np.zeros((610, 460))
MAP[0, :] = 100
MAP[609, :] = 100
MAP[:, 0] = 100
MAP[:, 459] = 100
MAP_T[:, :] = np.inf
Kp_r = 0
Kp_theta = 0
Kd_r = 0
Kd_theta = 0 

print('Server Started.')
botIDs = StartServer(1)
print('Bots Connected.')
bots = []

for id in botIDs:
    bots.append(Bot(id))
print('Bots detected')

boxIDs = [5]
dest=np.random.randint(30, 80, (4, 2))
boxs = []
print('Boxes detected')


for id in boxIDs:
    boxs.append(Box(id))
for i in range(len(boxs)):
    boxs[i].dest=dest[i]
    bots[i].assignBox(boxs[i])

print('Task assigned')

p=[]
t=[]
tb=[]

for i in range(len(bots)):
    p1, t1, tb1 = bots[i].createPath(MAP, MAP_T)
    p.append(p1)
    # print(MAP[list(map(list, p[i].T))[0],list(map(list, p[i].T))[1]])
    t.append(t1)
    tb.append(tb1)

    MAP[list(map(list, p[i].T))[0],list(map(list, p[i].T))[1]] = 100
    #print(MAP_T[p[i]],t[i].shape)
    MAP_T[list(map(list, p[i].T))[0],list(map(list, p[i].T))[1]] = t[i]
    MAP_T[p[i][-1][0], p[i][-1][1]] = np.inf

print('Path planned')


plt.imshow(camera.getEnvironment())
plt.plot(p1[:, 0], p1[:, 1])
plt.xlim(0, 610)
plt.ylim(0, 460)
plt.show()

tic = time.time()

while True:
    for bot in bots:
        try:
            toc = time.time()
            t = toc - tic
            #if int(t%5)==0 and Kd_r<5:
            #    Kd_r+=0
            print(f"{Kd_r=},{Kp_r=},{t=}")
            bot.updatePos()
            exp_pos = bot.position(t)
            dr = bot.distFromPoint(exp_pos)/5.0
            dtheta = bot.orientation(t) - bot.theta
            # V = Kp_r*dr - Kd_r*bot.speed + 100
            V = Kp_r*dr - Kd_r*bot.speed
            #print(f"V={V}")

            # Vleft = int(V + Kp_theta*dtheta + Kd_theta*bot.omega)
            # Vright = int(V - Kp_theta*dtheta - Kd_theta*bot.omega)
            # print(f"{dtheta=}, {bot.theta=}, {bot.omega=}")
            Vleft = int(200)
            Vright = int(-200)
            if Vleft > 255:
                Vleft = 255
            if Vleft < -255:
                Vleft = -255
            if Vright > 255:
                Vright = 255
            if Vright < -255:
                Vright = -255
            print(f"Vleft={Vleft}  Vright={Vright}")
            control(bot.id,botIDs[bot.id],Vright,Vleft)
        except Exception as e:
            print("ERROR",e, e.args)
            control(bot.id,botIDs[bot.id],0,0)
        time.sleep(0.01)

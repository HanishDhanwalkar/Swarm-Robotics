import numpy as np
import matplotlib.pyplot as plt
import time
from camera import MobileCamera
from bots import Bot, Box
from server import StartServer


class Run:
    def __init__(self, camIP, mapW, mapH, numBots, boxIDs, dests, debug) -> None:
        print('Run Started.')
        self.camera = MobileCamera(f"http://{camIP}/video", debug=debug)
        self.debug = debug
        print('Camera Connected.')
        self.mapW = mapW
        self.mapH = mapH
        self.numBots = numBots
        self.map, self.mapT = self.CreateMap()
        self.bots = self.connectBots()
        self.boxes = self.connectBoxes(boxIDs)
        self.assignTasks(dests)
        self.planPath()

    def CreateMap(self):
        MAP = np.zeros((self.mapW, self.mapH))
        MAP_T = np.zeros((self.mapW, self.mapH))
        MAP[0, :] = 100
        MAP[self.mapW-1, :] = 100
        MAP[:, 0] = 100
        MAP[:, self.mapH-1] = 100
        MAP_T[:, :] = np.inf
        return MAP, MAP_T

    def connectBots(self):
        print('Server Started.')
        if self.debug:
            botIDs = {4 : '192.168.122.164:8080'}
        else:
            botIDs = StartServer(self.numBots)
        print('Bots Connected.')

        bots = []
        for id in botIDs:
            bots.append(Bot(id, botIDs[id]))
        print('Bots detected')

        return bots

    def connectBoxes(self, ids):
        boxes = []
        for id in ids:
            boxes.append(Box(id))
        print('Boxes detected')

        return boxes

    def assignTasks(self, dests):
        for i in range(len(self.boxes)):
            self.boxes[i].dest = dests[i]
            self.bots[i].assignBox(self.boxes[i])
        print('Task assigned')

    def planPath(self):
        p = []
        t = []
        tb = []

        for i in range(len(self.bots)):
            p1, t1, tb1 = self.bots[i].createPath(self.map, self.mapT)
            p.append(p1)
            t.append(t1)
            tb.append(tb1)

            self.map[list(map(list, p[i].T))[0],
                     list(map(list, p[i].T))[1]] = 100
            self.mapT[list(map(list, p[i].T))[0],
                      list(map(list, p[i].T))[1]] = t[i]
            self.mapT[p[i][-1][0], p[i][-1][1]] = np.inf

        print('Path planned')

        plt.imshow(self.camera.getEnvironment())
        plt.plot(p1[:, 0], p1[:, 1])
        plt.xlim(0, self.mapW)
        plt.ylim(0, self.mapH)
        plt.show()

    def run(self, Kp_r, Kp_theta, Kd_r, Kd_theta):
        tic = time.time()
        while True:
            for bot in self.bots:
                try:
                    toc = time.time()
                    t = toc - tic
                    # if int(t%5)==0 and Kd_r<5:
                    #    Kd_r+=0
                    print(f"{Kd_r=},{Kp_r=},{t=}")
                    bot.updatePos()
                    exp_pos = bot.position(t)
                    dr = bot.distFromPoint(exp_pos)/5.0
                    dtheta = bot.orientation(t) - bot.theta
                    # V = Kp_r*dr - Kd_r*bot.speed + 100
                    V = Kp_r*dr - Kd_r*bot.speed
                    # print(f"V={V}")

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
                    bot.control(Vright, Vleft)
                except Exception as e:
                    print("ERROR", e, e.args)
                    bot.control(0, 0)
                    exit(0)
                except KeyboardInterrupt:
                    print("Keyboard Interrupt")
                    bot.control(0, 0)
                    exit(0)
                time.sleep(0.01)

    def plot3D(self):
        figure2 = plt.figure(figsize=(6, 6))
        obstacles = np.argwhere(self.map == 100)

        ax2 = figure2.add_subplot(111, projection='3d')
        ax2.set_xlim(-1, self.mapW+1)
        ax2.set_ylim(-1, self.mapH+1)
        ax2.scatter(obstacles[:, 0], obstacles[:, 1], [0],
                    marker='.', color='k', zorder=2)

        plotBots, plotBoxes, plotDests, plotPaths = [], [], [], []

        for bot in self.bots:
            t=np.linspace(0,bot.t[-1],1000)
            path=bot.position(t)
            plotBots.append(ax2.scatter([bot.pos[0]], [bot.pos[1]], [0], marker='o',
                                        label=f'Bot {bot.id}', zorder=3))
            plotBoxes.append(ax2.scatter([bot.box.pos[0]], [bot.box.pos[1]], [bot.box.reachtime], marker='d',
                                         label=f'Box {bot.id}', zorder=3))
            plotDests.append(ax2.scatter([bot.target[0]], [bot.target[1]], [bot.t[-1]], marker='*',
                                         label=f'Dest {bot.id}', zorder=3))
            plotPaths.append(ax2.plot(path[:, 0], path[:, 1], t,
                             zorder=2))

        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

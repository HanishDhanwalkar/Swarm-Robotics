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
            botIDs = {4 : '192.168.122.164:1111',5 : '192.168.122.164:1111',6 : '192.168.122.164:1111'}
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
        for path in p:
            plt.plot(path[:, 0], path[:, 1])
        plt.xlim(0, self.mapW)
        plt.ylim(0, self.mapH)
        plt.show()

    def plotControls(self,t,dtheta,vl=[],vr=[],dr=[]):
        fig3 = plt.figure(figsize=(10,6))
        ax=fig3.add_subplot(1,1,1)
        ax.plot(t,dtheta,label='dtheta')
        if len(vr)>0:
            ax.plot(t,vr,label='vr')
        if len(vl)>0:
            ax.plot(t,vl,label='vl')
        if len(dr)>0:
            ax.plot(t,dr,label='dr')
        plt.legend()
        plt.show()

    def run(self, Kp_r, Kp_theta, Kd_r, Kd_theta):
        tic = time.time()
        vr=[]
        vl=[]
        dt=[]
        Dr=[]
        T=[]
        vinL=125
        vinR=125
        while True:
            for bot in self.bots:
                try:
                    toc = time.time()
                    t = toc - tic
                    # if int(t%10)==0:
                    #    Kd_theta+=1
                    print(f"{Kd_r=},{Kp_r=},{t=}")
                    bot.updatePos()
                    exp_pos = bot.position(t)
                    dr = bot.distFromPoint(exp_pos)/5.0
                    # dtheta = bot.orientation(t) - bot.theta
                    dtheta=90-bot.theta
                    print(f"{dtheta=}, {bot.theta=}")
                    
                    V = Kp_r*dr - Kd_r*bot.speed 
                    Dr.append(dr)
                    T.append(t)
                    dt.append(dtheta)
                    if abs(dtheta) <= 10:
                        dtheta=0

                    Vright = int(V - Kp_theta*dtheta - Kd_theta*bot.omega)
                    Vleft = int(V + Kp_theta*dtheta + Kd_theta*bot.omega)
    
                    if Vleft > 255:
                        Vleft = 255
                    if Vleft < -255:
                        Vleft = -255
                    if Vright > 255:
                        Vright = 255
                    if Vright < -255:
                        Vright = -255

                    Vright=np.sign(Vright)*(abs(Vright)*145/255+110)
                    Vleft=np.sign(Vleft)*(abs(Vleft)*145/255+110)

                    vr.append(Vright)
                    vl.append(Vleft)
                    print(f"Vleft={Vleft}  Vright={Vright}")
                    bot.control(Vright,Vleft)
                except Exception as e:
                    print("ERROR", e, e.args)
                    bot.control(0, 0)
                    self.plotControls(T,dt)
                    exit(0)
                except KeyboardInterrupt:
                    print("Keyboard Interrupt")
                    bot.control(0, 0)
                    self.plotControls(T,dt)
                    exit(0)
                # time.sleep(0.05)
                # bot.control(0, 0)
        self.plotControls(T,dt)

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

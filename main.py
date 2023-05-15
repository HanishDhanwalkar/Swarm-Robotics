import numpy as np
from aStar import Map
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter, FuncAnimation
from bots import Bot, Box
import seaborn as sns

MAP = np.zeros((25, 25))
MAP_T = np.zeros((25, 25))
MAP[0, :] = 100
MAP[24, :] = 100
MAP[:, 0] = 100
MAP[:, 24] = 100
MAP_T[:, :] = -1

obstacles = np.argwhere(MAP == 100)

dest1 = [10, 16]
box1 = Box(23, 3)
bot1 = Bot(3, 3)
box1.dest = dest1
bot1.assignBox(box1)

dest2 = [20, 23]
box2 = Box(23, 6)
bot2 = Bot(3, 5)
box2.dest = dest2
bot2.assignBox(box2)

dest3 = [10, 13]
box3 = Box(20, 2)
bot3 = Bot(3, 18)
box3.dest = dest3
bot3.assignBox(box3)

p2, t2, tb2 = bot2.createPath(MAP, MAP_T)

MAP[list(map(list, p2.T))] = 100
MAP_T[list(map(list, p2.T))] = t2

p1, t1, tb1 = bot1.createPath(MAP, MAP_T)

MAP[list(map(list, p1.T))] = 100
MAP_T[list(map(list, p1.T))] = t1

p3, t3, tb3 = bot3.createPath(MAP, MAP_T)

# figure = plt.figure(figsize=(6, 6))
# ax = figure.add_subplot(111,projection='3d')
# ax.set_xlim(-1, 25)
# ax.set_ylim(-1, 25)
# b1=ax.scatter([bot1.pos[0]], [bot1.pos[1]],[0], marker='o',
#            color='g', label='Bot 1', zorder=3)
# b2=ax.scatter([bot2.pos[0]], [bot2.pos[1]],[0], marker='o',
#            color='r', label='Bot 2', zorder=3)
# bx1=ax.scatter([box1.pos[0]], [box1.pos[1]], [tb1],marker='d',
#            color='g', label='Box 1', zorder=3)
# bx2=ax.scatter([box2.pos[0]], [box2.pos[1]], [tb2],marker='d',
#            color='r', label='Box 2', zorder=3)
# des1=ax.scatter([dest1[0]], [dest1[1]], [t1[-1]],marker='*',
#            color='g', label='Dest 1', zorder=3)
# des2=ax.scatter([dest2[0]], [dest2[1]], [t2[-1]],marker='*',
#            color='r', label='Dest 2', zorder=3)
# ax.scatter(obstacles[:, 0], obstacles[:, 1],[0],
#            marker='.', color='k', zorder=2)
# ax.plot(p1[:, 0], p1[:, 1],t1, color='g', label='Path 1', zorder=2)
# ax.plot(p2[:, 0], p2[:, 1],t2, color='r', label='Path 2', zorder=2)
# plt.xlabel('x')
# plt.ylabel('y')
# ax.set_zlabel('time')
# plt.legend(loc='lower right')


figure2 = plt.figure(figsize=(6, 6))
ax2 = figure2.add_subplot(111)
ax2.set_xlim(-1, 25)
ax2.set_ylim(-1, 25)
b1 = ax2.scatter([bot1.pos[0]], [bot1.pos[1]], marker='o',
                 color='g', label='Bot 1', zorder=3)
b2 = ax2.scatter([bot2.pos[0]], [bot2.pos[1]], marker='o',
                 color='r', label='Bot 2', zorder=3)
b3 = ax2.scatter([bot3.pos[0]], [bot3.pos[1]], marker='o',
                 color='b', label='Bot 2', zorder=3)
bx1 = ax2.scatter([box1.pos[0]], [box1.pos[1]], marker='d',
                  color='g', label='Box 1', zorder=3)
bx2 = ax2.scatter([box2.pos[0]], [box2.pos[1]], marker='d',
                  color='r', label='Box 2', zorder=3)
bx3 = ax2.scatter([box3.pos[0]], [box3.pos[1]], marker='d',
                  color='b', label='Box 2', zorder=3)
des1 = ax2.scatter([dest1[0]], [dest1[1]], marker='*',
                   color='g', label='Dest 1', zorder=3)
des2 = ax2.scatter([dest2[0]], [dest2[1]], marker='*',
                   color='r', label='Dest 2', zorder=3)
des3 = ax2.scatter([dest3[0]], [dest3[1]], marker='*',
                   color='b', label='Dest 2', zorder=3)
ax2.scatter(obstacles[:, 0], obstacles[:, 1],
            marker='.', color='k', zorder=2)
ax2.plot(p1[:, 0], p1[:, 1], color='g', label='Path 1', zorder=2)
ax2.plot(p2[:, 0], p2[:, 1], color='r', label='Path 2', zorder=2)
ax2.plot(p3[:, 0], p3[:, 1], color='b', label='Path 3', zorder=2)
plt.xlabel('x')
plt.ylabel('y')

# # plt.legend()
# plt.show()


def animate(i):
    l1 = min(i, 10*bot1.t[-1])
    l2 = min(i, 10*bot2.t[-1])
    l3 = min(i, 10*bot3.t[-1])

    b1.set_offsets(bot1.returnPos(l1))
    b2.set_offsets(bot2.returnPos(l2))
    b3.set_offsets(bot3.returnPos(l3))


    bx1.set_offsets([box1.pos[0], box1.pos[1]])
    bx2.set_offsets([box2.pos[0], box2.pos[1]])
    bx3.set_offsets([box3.pos[0], box3.pos[1]])


anim = FuncAnimation(figure2, animate, 10 *
                     int(max(bot2.t[-1], bot1.t[-1], bot3.t[-1])+2), interval=2)
anim.save('anim.mp4', FFMpegWriter())

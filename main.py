import numpy as np
from aStar import Map
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter,FuncAnimation
from bots import Bot,Box

MAP=np.zeros((25,25))
MAP_T=np.zeros((25,25))
MAP[0,:]=100
MAP[24,:]=100
MAP[:,0]=100
MAP[:,24]=100
MAP_T[:,:]=np.inf

obstacles=np.argwhere(MAP==100)

dest1=[23,23]
box1=Box(6,20)
bot1=Bot(3,3)
box1.dest=dest1
bot1.assignBox(box1)
p1,t1,tb1=bot1.createPath(MAP,MAP_T)

MAP[list(map(list,p1.T))]=100
MAP_T[list(map(list,p1.T))]=t1


dest2=[20,23]
box2=Box(16,6)
bot2=Bot(3,5)
box2.dest=dest2
bot2.assignBox(box2)
p2,t2,tb2=bot2.createPath(MAP,MAP_T)


figure = plt.figure(figsize=(6, 6))
ax = figure.add_subplot(111,projection='3d')
ax.set_xlim(-1, 25)
ax.set_ylim(-1, 25)
b1=ax.scatter([bot1.pos[0]], [bot1.pos[1]],[0], marker='o',
           color='g', label='Bot 1', zorder=3)
b2=ax.scatter([bot2.pos[0]], [bot2.pos[1]],[0], marker='o',
           color='r', label='Bot 2', zorder=3)
bx1=ax.scatter([box1.pos[0]], [box1.pos[1]], [tb1],marker='d',
           color='g', label='Box 1', zorder=3)
bx2=ax.scatter([box2.pos[0]], [box2.pos[1]], [tb2],marker='d',
           color='r', label='Box 2', zorder=3)
des1=ax.scatter([dest1[0]], [dest1[1]], [t1[-1]],marker='*',
           color='g', label='Dest 1', zorder=3)
des2=ax.scatter([dest2[0]], [dest2[1]], [t2[-1]],marker='*',
           color='r', label='Dest 2', zorder=3)
ax.scatter(obstacles[:, 0], obstacles[:, 1],[0],
           marker='.', color='k', zorder=2)
ax.plot(p1[:, 0], p1[:, 1],t1, color='g', label='Path 1', zorder=2)
ax.plot(p2[:, 0], p2[:, 1],t2, color='r', label='Path 2', zorder=2)
# plt.xlabel('x')
# plt.ylabel('y')
# ax.set_zlabel('time')
# plt.legend(loc='lower right')

# def animate(i):
#     l1=min(i,len(bot1.path)-1)
#     l2=min(i,len(bot2.path)-1)
#     bot1.updatePos(l1)
#     bot2.updatePos(l2)
#     b1.set_offsets([bot1.pos[0],bot1.pos[1]])
#     b2.set_offsets([bot2.pos[0],bot2.pos[1]])
#     bx1.set_offsets([box1.pos[0],box1.pos[1]])
#     bx2.set_offsets([box2.pos[0],box2.pos[1]])


# anim = FuncAnimation(figure, animate, max(len(bot1.path),len(bot2.path)), interval=20)
# anim.save('anim.mp4', FFMpegWriter())

figure2 = plt.figure(figsize=(6, 6))
ax2 = figure2.add_subplot(111)
ax2.set_xlim(-1, 25)
ax2.set_ylim(-1, 25)
b1=ax2.scatter([bot1.pos[0]], [bot1.pos[1]], marker='o',
           color='g', label='Bot 1', zorder=3)
b2=ax2.scatter([bot2.pos[0]], [bot2.pos[1]], marker='o',
           color='r', label='Bot 2', zorder=3)
bx1=ax2.scatter([box1.pos[0]], [box1.pos[1]],marker='d',
           color='g', label='Box 1', zorder=3)
bx2=ax2.scatter([box2.pos[0]], [box2.pos[1]],marker='d',
           color='r', label='Box 2', zorder=3)
des1=ax2.scatter([dest1[0]], [dest1[1]],marker='*',
           color='g', label='Dest 1', zorder=3)
des2=ax2.scatter([dest2[0]], [dest2[1]],marker='*',
           color='r', label='Dest 2', zorder=3)
ax2.scatter(obstacles[:, 0], obstacles[:, 1],
           marker='.', color='k', zorder=2)
ax2.plot(p1[:, 0], p1[:, 1], color='g', label='Path 1', zorder=2)
ax2.plot(p2[:, 0], p2[:, 1], color='r', label='Path 2', zorder=2)
# plt.xlabel('x')
# plt.ylabel('y')

plt.legend()
plt.show()
import numpy as np
from aStar import Map
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter, FuncAnimation
from bots import Bot, Box
import seaborn as sns
import time

MAP = np.zeros((25, 25))
MAP_T = np.zeros((25, 25))
MAP[0, :] = 100
MAP[24, :] = 100
MAP[:, 0] = 100
MAP[:, 24] = 100
MAP_T[:, :] = np.inf

numBots=4
obstacles = np.argwhere(MAP == 100)

dests = [[12, 10], [12, 11], [12, 12], [13, 10]]
bxs = np.random.randint(1, 24, (4, 2))
bts = np.random.randint(1, 24, (4, 2))

boxes = []
bots = []

for i in range(numBots):
    boxes.append(Box(*bxs[i]))
    bots.append(Bot(*bts[i]))
    boxes[i].dest = dests[i]
    bots[i].assignBox(boxes[i])

bots=sorted(bots,key= lambda x: x.Dist(x.box)+x.box.Dist(x.target))

p, t, tb = [], [], []

start=time.time()
for i in range(numBots):
    p1, t1, tb1 = bots[i].createPath(MAP, MAP_T)
    p.append(p1)
    t.append(t1)
    tb.append(tb1)

    MAP[list(map(list, p[i].T))] = 100
    MAP_T[list(map(list, p[i].T))] = t[i]
    MAP_T[p[i][-1][0], p[i][-1][1]] = np.inf
end=time.time()

print(f'Processing time: {end-start}')

figure2 = plt.figure(figsize=(6, 6))
ax2 = figure2.add_subplot(111,projection='3d')
ti=np.linspace(0,bots[1].t[-1])
path=bots[1].position(ti)
x=path[:,0]
y=path[:,1]
theta=bots[1].orientation(ti)
ax2.scatter(x,y,ti)
ax2.set_xlim(-1, 25)
ax2.set_ylim(-1, 25)
ax2.scatter(obstacles[:, 0], obstacles[:, 1], [0],
            marker='.', color='k', zorder=2)

# plotBots, plotBoxes, plotDests, plotPaths = [], [], [], []
# clrs = ['r', 'g', 'b', 'k']

# for i in range(numBots):
#     plotBots.append(ax2.scatter([bots[i].pos[0]], [bots[i].pos[1]],[0], marker='o',
#                     color=clrs[i], label=f'Bot {i+1}', zorder=3))
#     plotBoxes.append(ax2.scatter([bots[i].box.pos[0]], [bots[i].box.pos[1]],[bots[i].box.reachtime], marker='d',
#                                  color=clrs[i], label=f'Box {i+1}', zorder=3))
#     plotDests.append(ax2.scatter([bots[i].target[0]], [bots[i].target[1]],[t[i][-1]], marker='*',
#                                  color=clrs[i], label=f'Dest {i+1}', zorder=3))
#     plotPaths.append(ax2.plot(p[i][:, 0], p[i][:, 1],t[i],
#                      color=clrs[i], label='Path 1', zorder=2))

# plt.xlabel('x')
# plt.ylabel('y')

# maxtime = 0
# for i in range(numBots):
#     print(bots[i].t[-1])
#     if bots[i].t[-1] > maxtime:
#         maxtime = bots[i].t[-1]

plt.show()


# def animate(i):
#     for j in range(numBots):
#         lim = min(i, 10*bots[j].t[-1])
#         plotBots[j].set_offsets(bots[j].returnPos(lim))
#         plotBoxes[j].set_offsets([boxes[j].pos[0], boxes[j].pos[1]])


# anim = FuncAnimation(figure2, animate, 10 * int(maxtime+2), interval=2)
# anim.save('anim.mp4', FFMpegWriter())

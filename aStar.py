import numpy as np
import warnings
warnings.filterwarnings('ignore')


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fscore = np.inf
        self.gscore = np.inf
        self.hscore = np.inf
        self.parent = None
        self.t = 0

    def Dist(self, point):
        delX = self.x-point.x
        delY = self.y-point.y
        return np.sqrt(delX**2+delY**2)

    def getHscore(self, dest):
        return self.Dist(dest)

    def getFscore(self, dest):
        return self.gscore+self.getHscore(dest)

    def getNeighbours(self):
        up = [[self.x+i, self.y+1] for i in [-1, 0, 1]]
        bel = [[self.x+i, self.y-1] for i in [-1, 0, 1]]
        mid = [[self.x-i, self.y] for i in [-1, 1]]

        neighbours = up+bel+mid
        return list(map(list, np.array(neighbours).T))


class Map:
    def __init__(self, w, h, map, init, fin, mapT, tStart=0):
        self.map = map
        self.nodes = np.zeros((w, h), dtype=Node)
        for i in range(w):
            for j in range(h):
                self.nodes[i, j] = Node(i, j)
        self.w = w
        self.h = h
        self.init = self.nodes[init[0], init[1]]
        self.fin = self.nodes[fin[0], fin[1]]
        self.init.gscore = 0
        self.init.t = tStart
        self.mapT = mapT
        self.init.fscore = self.init.getFscore(self.fin)
        self.clearence = 3
        self.speed = 6

    def Dist(self, p1, p2):
        deltaX = p1[0]-p2[0]
        deltaY = p1[1]-p2[1]
        return np.sqrt(deltaX**2+deltaY**2)

    def isCollision(self, p, point: Node):
        t = point.t+self.Dist(p, np.array([self.clearence, self.clearence]))/self.speed
        if self.mapT[p[0]+point.x-self.clearence, p[1]+point.y-self.clearence] == np.inf or abs(self.mapT[p[0]+point.x-self.clearence, p[1]+point.y-self.clearence]-t) < 0.5:
            return self.Dist(p, np.array([self.clearence, self.clearence]))
        return np.inf

    def neighbourOfObstacle(self, point):
        hood = self.map[point.x-self.clearence:point.x+self.clearence, point.y-self.clearence:point.y+self.clearence]
        obstacles = np.argwhere((hood == 100))
        if len(obstacles) == 0:
            return 0
        closest = sorted(obstacles, key=lambda x: self.isCollision(x, point))[0]
        return 25/self.Dist(closest, np.array([self.clearence, self.clearence]))

    def updatedGScore(self, init: Node, new: Node):
        t = init.t+init.Dist(new)/self.speed
        if self.map[new.x, new.y] == 100 and (self.mapT[new.x, new.y] == np.inf or abs(self.mapT[new.x, new.y]-t) < 0.5):
            return np.inf
        return init.gscore+self.neighbourOfObstacle(new)+1

    def constructPath(self):
        path = []
        t_stamps = []
        curr = self.fin

        while curr.parent != None:
            path.append([curr.x, curr.y])
            t_stamps.append(curr.t)
            curr = curr.parent
        path.append([curr.x, curr.y])
        t_stamps.append(curr.t)
        return np.array(path), np.array(t_stamps)

    def getPath(self):
        self.openSet = [self.init]
        self.closedSet = []
        while len(self.openSet) != 0:
            curr = sorted(self.openSet, key=lambda x: x.fscore)[0]
            if curr.getHscore(self.fin) <= 10**-6:
                return self.constructPath()

            del self.openSet[self.openSet.index(curr)]

            neighbours = curr.getNeighbours()
            neighboursX=neighbours[0]
            neighboursY=neighbours[1]
            neighbours = self.nodes[neighboursX,neighboursY]

            for neighbour in neighbours:
                newGScore = self.updatedGScore(curr, neighbour)
                if newGScore < neighbour.gscore:
                    neighbour.parent = curr
                    neighbour.gscore = newGScore
                    neighbour.t = curr.t+neighbour.Dist(curr)/self.speed
                    neighbour.fscore = neighbour.getFscore(self.fin)
                    if neighbour not in self.openSet:
                        self.openSet.append(neighbour)

        return None

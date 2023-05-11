import numpy as np
from aStar import Map

class Box:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.pos=[self.x,self.y]
        self.dest=None
    
    def Dist(self,point):
        delX=self.x-point[0]
        delY=self.y-point[1]
        return np.sqrt(delX**2+delY**2)


class Bot:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.pos=[self.x,self.y]
        self.box=None
        self.target=None
        self.path=None
        self.t=None
        self.reachedBox=False

    def Dist(self,point):
        delX=self.x-point.x
        delY=self.y-point.y
        return np.sqrt(delX**2+delY**2)
    
    def assignBox(self,box):
        self.box=box
        self.target=box.dest

    def updatePos(self,i):
        self.x=self.path[i][0]
        self.y=self.path[i][1]
        self.pos=[self.x,self.y]
        if self.x==self.box.x and self.y==self.box.y:
            self.reachedBox=True

        if self.reachedBox:
            self.box.x=self.x
            self.box.y=self.y
            self.box.pos=[self.x,self.y]

    def path2box(self,map,mapT):
        w,h=map.shape
        m=Map(w,h,map,self.pos,self.box.pos,mapT)
        path,t=m.getPath()
        return path[::-1],t[::-1]
    
    def path2target(self,map,mapT,tStart):
        w,h=map.shape
        m=Map(w,h,map,self.box.pos,self.target,mapT,tStart)
        path,t=m.getPath()
        return path[::-1],t[::-1]
    
    def createPath(self,map,mapT):
        path1,t1=self.path2box(map,mapT)
        path2,t2=self.path2target(map,mapT,t1[-1])
        self.path=np.insert(path2,0,path1,axis=0)
        self.t=np.insert(t2,0,t1,axis=0)
        return self.path,self.t,t1[-1]
   
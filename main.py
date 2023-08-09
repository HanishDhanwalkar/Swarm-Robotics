from Runner import Run
import numpy as np

camera = '192.168.0.190:1111'
mapDims = [610, 460]
numBots = 1
boxes = [6, 7]
destinations = [[100,68],[68,100]] #np.random.randint(30, 300, (4, 2))

newRun = Run(camera, *mapDims, numBots, boxes, destinations, debug=True)
newRun.plot3D()

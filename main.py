from Runner import Run
import numpy as np

camera = '192.168.0.190:1111'
mapDims = [610, 460]
numBots = 1
boxes = [4]
destinations = np.random.randint(50, 300, (3, 2))

newRun = Run(camera, *mapDims, numBots, boxes, destinations, debug=False)
newRun.plot3D()
newRun.run(-15,3,0,0)

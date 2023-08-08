from Runner import Run
import numpy as np

camera = '192.168.122.86:1111'
mapDims = [610, 460]
numBots = 1
boxes = [5]
destinations = np.random.randint(30, 80, (4, 2))

newRun = Run(camera, *mapDims, numBots, boxes, destinations, debug=True)
newRun.plot3D()

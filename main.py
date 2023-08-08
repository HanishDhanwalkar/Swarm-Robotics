from trialRun import Run
import numpy as np

newRun = Run('192.168.122.86:1111',610,460,1,[5],np.random.randint(30, 80, (4, 2)),True)
newRun.run(0,0,0,0)

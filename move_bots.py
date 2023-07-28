# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 20:58:08 2023

@author: Tanmay Ganguli
"""

#import libraries
import numpy as np
import cv2 as cv
import cv2.aruco as aruco
from bots import Bot,Box
from aStar import Map


#define constants
num_box = 4
num_bot = 4
num_corner = 4
corner_ids = [1,2,3,4]
bot_ids = [5,6,7,8]
box_ids = [9,10,11,12]
boxes = []
box_locs = []
bots = []
bot_locs = []

MAP = np.zeros((500,500))
MAP_T = np.zeros((500,500))
MAP[:,0] = 100
MAP[:,499] = 100
MAP[0,:] = 100
MAP[499,:] = 100
MAP_T[:,:] = np.inf

targets = [[100,0],[400,0],[0,100],[0,400]]
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
parameters = aruco.DetectorParameters()

path_not_planned = True


def read_aruco(frame):
    #detect the aruco markers of corners, bots,boxes and return a list of them
    detector = aruco.DetectorParameters(aruco_dict,parameters)
    corners,ids,rejected = detector.detectMarkers(frame,aruco_dict,parameters)
    detected = dict(zip(ids,corners))
    detected = dict(sorted(detected.items()))
    detected_ids = detected.keys()
    corners = detected.values()
    if detected_ids == corner_ids + bot_ids + box_ids:
        return (12,zip(detected_ids,corners))
    return len(detected_ids),list(zip(detected_ids,corners))  

def transform(frame,corner_loc,bot_loc,box_loc):
    
    return bot_loc,box_loc

def send_command(V,url):
    return 

src = 'string'
cap = cv.VideoCapture(src)
#not_done = True

#detect all the bots and boxes initially and make assignments
while True:
    ret, frame = cap.read()
    num_ids, list_items = read_aruco(frame)
    #element of list: (id,(topLeft,topRight,bottomLeft,bottomRight))
    if num_ids == 12:
        corner_pts = []
        for index in range(3):
            id = list_items[index][0]
            corners = list_items[index][1]
            [xm,ym] = np.mean(corners,axis=0)#mid pointof corner arucos
            corner_pts.append([xm,ym])
        
        
        for i in range(8,12):
            id = list_items[i][0]
            corners = list_items[i][1]
            [xm,ym] = np.mean(corners,axis=0)#mid point of box location
            box_locs.append([xm,ym])
            boxes.append(Box(xm,ym,id))
            boxes[i].dest = targets[i]
        
        for i in range(4,8):
            id = list_items[i][0]
            corners = list_items[i][1]
            [xm,ym] = np.mean(corners,axis=0)#mid point of bot location
            bot_locs.append([xm,ym])
            bots.append(Bot(xm,ym,id))
            
        #transform coordinates
        transform(frame,corner_pts,boxes,bots)
        #assign boxes
        bots[i].assignBox(boxes[i])
        bots = sorted(bots, key= lambda x:x.Dist(x.Box)+x.Box.Dist(x.target))
        
        #plan the paths
        for i in range(num_bot):
            _,_,t1 = bots[i].createPath()
        break

while True:
    ret, frame = cap.read()
    if ret:
        
        
        #get image, detect aruco markers, corners, bots, boxes
        
        num_ids,list_items = read_aruco(frame)
        #element of list: (id,(topLeft,topRight,bottomLeft,bottomRight))
        if num_ids ==12:
            #list down the corners
            corner_pts = []
            for index in range(3):
                id = list_items[index][0]
                corners = list_items[index][1]
                [xm,ym] = np.mean(corners,axis=0)#mid pointof corner arucos
                corner_pts.append([xm,ym])
                #coordinate transform
                transform(frame,corner_pts,list_items)
                #update the positions of the bots and boxes
                for i in range(4,8):
                    bots[i].updatePos(np.mean(list_items[i][1],axis=0))
                for i in range(8,12):
                    boxes[i].updatePos(np.mean(list_items[i][1],axis=0))
            
            
            
            
                
            #calculate distance of the bots from expected coordinates and angle of rotation 
            #from expected angle(mostly = 0)
            for i in range(4,7):
                x_ex, y_ex = bots[i].returnPos(t) #expected position of bot at time t
                pos_ex = [x_ex,y_ex]
                r = bots[i].Dist(pos_ex)
                vel = bots[i].speed
                #determine control voltage for each wheel
                V = int(Kp*r + Kd*vel) #control voltage, KP, Kd, Ki
                if V > 255:
                    V = 255
                if V < 0:
                    V = 0
                
                #send command to respective esp's
                send_command(V,url)
                
                
                
        else:
        
#start loop
























#if a bot is near its box, switch on electromagnet circuit
#circuit remains on until bot reaches target
#PID cosnatnts may be different when box is attached to bot 

#follow up to above task, check if box is being carried by the bot,







 




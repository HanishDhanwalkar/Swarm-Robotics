import cv2 as cv
import cv2.aruco as aruco
import numpy as np

def transformation(matrix,coordinate):
    x=np.ones((3,1))
    x[0]=coordinate[0]
    x[1]=coordinate[1]
    x_=np.matmul(matrix,x)
    return np.array([x_[0]/x_[2],x_[1]/x_[2]],dtype='int').reshape(2,)

def orientation(c1,c2,c3,c4):
    point1=(c1+c2)/2
    point2=(c3+c4)/2
    dif=point2-point1
    orient=np.degrees(np.arctan2(dif[1],dif[0]))
    return orient

def detectInsides(image):
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict,parameters)
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(image)
    markers={}


def detect(image):
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict,parameters)
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(image)
    order=[0,1,2,3]
    box=[0,0,0,0]
    for i in range(len(markerCorners)):
        image=cv.polylines(image,markerCorners[i].astype('int32'),True,(255,0,0),2)
        image=cv.putText(image,str(markerIds[i][0]),markerCorners[i].mean(axis=1)[0].astype('int32'),cv.FONT_HERSHEY_SIMPLEX,color=(0,0,255),thickness=1,fontScale=0.3)
        try:
            box[order.index(markerIds[i][0])]=markerCorners[i].mean(axis=1)[0].astype('int32')
        except:
            continue
    try:
        image=cv.polylines(image,np.array([box]),True,(0,255,0),2)
        if len(box)==4:
            inp=np.float32(box)
            out=np.float32([[0,0],[500,0],[500,500],[0,500]])
            matrix = cv.getPerspectiveTransform(inp, out)
            image = cv.warpPerspective(image, matrix, (500, 500))
            markers = detectInsides(image)
    except:
        return False,image , markers
    return True, image, markers


class MobileCamera:
    def __init__(self, camera):
        self.camera = camera
        self.cap = cv.VideoCapture(self.camera)

    def getImage(self):
        ref, frame = self.cap.read()
        frame = cv.resize(frame, (0, 0), fx=0.5, fy=0.5)
        value1,image, markers=detect(frame)
        while not value1 or len(markers)==0:
            ref, frame = self.cap.read()
            frame = cv.resize(frame, (0, 0), fx=0.5, fy=0.5)
            value1,image, markers=detect(frame)        
        self.cap.release()
        return markers,image

if __name__=='__main__':
    cam = MobileCamera("http://192.168.0.119:1111/video")
    markers,image=cam.getImage()
    # inp=cv.imread('images/aruc0.png')
    # val,image,markers=detect(inp)
    print(markers)
    cv.imshow('Area',image)
    cv.imwrite('images/aruco.jpg',image)
    cv.waitKey(0)
    cv.destroyAllWindows()

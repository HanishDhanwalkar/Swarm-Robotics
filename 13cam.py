import cv2 as cv
import cv2.aruco as aruco
import numpy as np


def detect(image):
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

    # Define the parameters for marker detection
    parameters = aruco.DetectorParameters()

    # Detect ArUco markers in the image
    detector = aruco.ArucoDetector(aruco_dict,parameters)

    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(image)
    # Draw the detected markers on the image
    order=[0,1,2,3]
    box=[0,0,0,0]
    markers={}
    for i in range(len(markerCorners)):
        image=cv.polylines(image,markerCorners[i].astype('int32'),True,(255,0,0),2)
        image=cv.putText(image,str(markerIds[i][0]),markerCorners[i].mean(axis=1)[0].astype('int32'),cv.FONT_HERSHEY_SIMPLEX,color=(0,0,255),thickness=4,fontScale=2)
        try:
            box[order.index(markerIds[i][0])]=markerCorners[i].mean(axis=1)[0].astype('int32')
        except:
            if markerIds[i][0]>3 and markerIds[i][0]<6:
                markers[markerIds[i][0]]=markerCorners[i].mean(axis=1)[0].astype('int32')
            continue
    try:
        image=cv.polylines(image,[np.array(box)],True,(0,255,0),2)
        if len(box)==4:
            inp=np.float32(box)
            out=np.float32([[0,0],[0,500],[500,500],[500,0]])
            matrix = cv.getPerspectiveTransform(inp, out)
            image = cv.warpPerspective(image, matrix, (500, 500))
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
        while not value1:
            ref, frame = self.cap.read()
            frame = cv.resize(frame, (0, 0), fx=0.5, fy=0.5)
            value1,image, markers=detect(frame)
            if value1:
                cv.imwrite('aruco.jpg',image)
            cv.imshow("mobileCam",image)
            if cv.waitKey(1) == ord('q'):
                break
        
        print(markers)
        self.cap.release()
        cv.destroyAllWindows()


cam = MobileCamera("http://192.168.93.192:1111/video")
cam.getImage()
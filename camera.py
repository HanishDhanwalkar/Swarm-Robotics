import cv2 as cv
import cv2.aruco as aruco
import numpy as np

class MobileCamera:
    def __init__(self, camera):
        self.camera = camera
        self.cap = cv.VideoCapture(self.camera)
        self.detector = self.CreateDetector()

    def getImage(self):
        ref, frame = self.cap.read()
        frame = cv.resize(frame, (0, 0), fx=0.5, fy=0.5)
        return frame

    def CreateDetector(self):
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        return detector.detectMarkers

    def getOrientation(self, marker):
        c1, c2, c3, c4 = marker[0]
        point1 = (c1+c2)/2
        point2 = (c3+c4)/2
        dif = point2-point1
        orient = np.degrees(np.arctan2(dif[1], dif[0]))
        return orient

    def getCorners(self, image):
        order = [0, 1, 2, 3]
        detectedCorners = [0]*4
        markerCorners, markerIds, rejectedCandidates = self.detector(image)
        markerIds=markerIds.reshape(-1,)
        for i in range(len(markerCorners)):
            try:
                detectedCorners[order.index(markerIds[i])] = markerCorners[i].mean(axis=1)[0].astype('int32')
            except:
                continue
        if not set(order).issubset(set(markerIds)):
            return []
        return detectedCorners

    def getEnvironment(self):
        image = self.getImage()
        corners = self.getCorners(image)
        while len(corners) != 4:
            image = self.getImage()
            corners = self.getCorners(image)
        inp = np.float32(corners)
        out = np.float32([[0, 0], [500, 0], [500, 500], [0, 500]])
        matrix = cv.getPerspectiveTransform(inp, out)
        image = cv.warpPerspective(image, matrix, (500, 500))
        return image

    def getObjects(self, image):
        markerCorners, markerIds, rejectedCandidates = self.detector(image)
        markers = {}
        for i in range(len(markerCorners)):
            center = markerCorners[i].mean(axis=1)[0].astype('int32')
            theta = self.getOrientation(markerCorners[i])
            markers[markerIds[i][0]] = (center[0], center[1], theta)
        return markers

    def getPosOfID(self, id):
        env = self.getEnvironment()
        objects = self.getObjects(env)
        try:
            return objects[id]
        except:
            return None


if __name__ == '__main__':
    cam = MobileCamera("http://192.168.0.119:1111/video")
    markers, image = cam.getImage()
    # inp=cv.imread('images/aruc0.png')
    # val,image,markers=detect(inp)
    print(markers)
    cv.imshow('Area', image)
    cv.imwrite('images/aruco.jpg', image)
    cv.waitKey(0)
    cv.destroyAllWindows()

import cv2
from cv2 import aruco
import matplotlib.pyplot as plt 
import time
import numpy as np

dist = [3.85014472e-01, -1.84429782e+01, 3.35959024e-03, -4.65459936e-03, 2.70496366e+02]

mtx = [[1.15144522e+03, 0.00000000e+00, 3.17341909e+02],
[0.00000000e+00, 1.14647292e+03, 1.80683419e+02],
[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]

# dist = [ 0.13997653, -0.85368874, -0.01555927,  0.00787213,  1.40654705]
# mtx = [[1.59563868e+03, 0.00000000e+00, 1.39525590e+03],
#  [0.00000000e+00, 1.58886346e+03, 8.54674678e+02],
#  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]

np_dist = np.asarray(dist)
np_mtx = np.asarray(mtx)

# cap = cv2.VideoCapture(0)

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
parameters =  aruco.DetectorParameters_create()

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output.mp4', fourcc, 25.0, (640,480))

# cap = cv2.VideoCapture()


# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()

while True:
    # Capture frame-by-frame
    # ret, frame = cap.read()
    frame = cv2.imread('2022-09-10-010229.jpg')
    # if frame is read correctly ret is True
    # if not ret:
    #     print("Can't receive frame (stream end?). Exiting ...")
    #     break
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    try:
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        # rvecs = np.array([])
        # tvecs = np.array([])
        
        [rvecs, tvecs, obj] = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, np_mtx, np_dist)
           
        rvec = rvecs[0]
        tvec = tvecs[0]
        
        frame_markers = cv2.drawFrameAxes(frame.copy(), np_mtx, np_dist, rvec, tvec, length=0.04, thickness = 2)
        
        # frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners)

        # Display the resulting frame
        cv2.imshow('frame', frame_markers)
        time.sleep(0.05)
    except TypeError:
        #motion blur  
        time.sleep(0.00001)
    

    # out.write(frame_markers)
    
    if cv2.waitKey(1) == ord('q'):
        break
        
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()


"""
PWM values 

Rotate:
Left: 1430 
Right: 1550
Stop: 0 

Link_1

Left > 1760
Right < 1760
middle: 1760
Stop: 0
"""
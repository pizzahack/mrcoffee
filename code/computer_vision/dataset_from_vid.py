import cv2
import os
import sys
import shutil

try:

    try:
        path = sys.argv[1]
    except ValueError:
        print("Check if path is valid.")

    # skip frames using step size
    try:
        STEP_SIZE=int(sys.argv[2])
    except ValueError:
        print("Step size must be int value!")

    cap = cv2.VideoCapture(path)

    if os.path.isdir('dataset') == True:
        shutil.rmtree('dataset')

    if os.path.isdir('dataset') == False:
        os.mkdir('dataset')

    os.chdir('dataset')
    count=0

    while True:
        
        ret, frame = cap.read()
        
        if cap.isOpened() == False:
            print("Check if path is valid.")

        if not ret:
            break
        
        if count%STEP_SIZE == 0:
            cv2.imwrite('image_{0}.png'.format(count), frame)
            print('image_{0}.png'.format(count))
        count+=1

        if cv2.waitKey(1) == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

except IndexError:
    print("Missing path or step size.")

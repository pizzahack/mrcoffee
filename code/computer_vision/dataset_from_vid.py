import cv2
import os
import sys
import shutil

try:
    count = 0
    image_num = 0

    try:
        input = sys.argv[1:]
    except ValueError:
        print("Check if path is valid.")

    try:
        paths = input[:-1]
    except ValueError:
        print("Check if path is valid.")

    # skip frames using step size
    # if step_size = 0 than fps*multiplier
    try:
        step_size = int(input[len(input)-1:][0])
    except (ValueError, TypeError):
        print("Step size must be int value!")
    
    if os.path.isdir('dataset') == True:
        shutil.rmtree('dataset')

    if os.path.isdir('dataset') == False:
        os.mkdir('dataset')

    os.chdir('dataset')

    for path in paths:
        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        multiplier = 2
        
        if step_size == 0:
            step_size = int(fps*multiplier)

        while True:

            ret, frame = cap.read()

            if cap.isOpened() == False:
                print("Check if path is valid.")

            if not ret:
                break

            if count % step_size == 0:
                cv2.imwrite('image_{0}.png'.format(image_num), frame)
                print('image_{0}.png'.format(image_num))
                image_num += 1
            count += 1

            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()

except (IndexError, NameError):
    print("Missing path or step size.")

import cv2
import os
import sys
import shutil

try:

    try:
        PATH = sys.argv[1]
    except ValueError:
        print("Check if path is valid.")

    # skip frames using step size
    # if step_size = 0 than fps*multiplier
    try:
        STEP_SIZE = int(sys.argv[2])
    except ValueError:
        print("Step size must be int value!")

    if os.path.isdir('dataset') == True:
        shutil.rmtree('dataset')

    if os.path.isdir('dataset') == False:
        os.mkdir('dataset')

    cap = cv2.VideoCapture(PATH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    multiplier = 2
    count = 0
    image_num = 0

    if STEP_SIZE == 0:
        STEP_SIZE = int(fps*multiplier)

    os.chdir('dataset')

    while True:

        ret, frame = cap.read()

        if cap.isOpened() == False:
            print("Check if path is valid.")

        if not ret:
            break

        if count % STEP_SIZE == 0:
            cv2.imwrite('image_{0}.png'.format(image_num), frame)
            print('image_{0}.png'.format(image_num))
            image_num += 1
        count += 1

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()

except IndexError:
    print("Missing path or step size.")

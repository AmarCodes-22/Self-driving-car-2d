import os
import cv2 as cv
import numpy as np
import pyautogui
from time import time
from object_detection import get_needles, get_bounding_boxes, show_bounding_boxes
from window_capture import get_window_dimensions


IMAGES_PATH = os.path.join(os.getcwd(), 'data')
paths = {
    'mine_needle': os.path.join(IMAGES_PATH, 'needles', 'mine1.jpg'),
    'yellow_car1_needle': os.path.join(IMAGES_PATH, 'needles', 'yellow-car1.jpg'),
    'yellow_car2_needle': os.path.join(IMAGES_PATH, 'needles', 'yellow-car2.jpg'),
    'blue_car1_needle': os.path.join(IMAGES_PATH, 'needles', 'blue-car1.jpg'),
    'red_car1_needle': os.path.join(IMAGES_PATH, 'needles', 'red-car1.jpg'),
    'red_car2_needle': os.path.join(IMAGES_PATH, 'needles', 'red-car2.jpg'),
    'power1_needle': os.path.join(IMAGES_PATH, 'needles', 'power1.jpg'),
    'red_truck1_needle': os.path.join(IMAGES_PATH, 'needles', 'red-truck1.jpg'),
    'yellow_truck1_needle': os.path.join(IMAGES_PATH, 'needles', 'yellow-truck1.jpg')
}

#* Defining needles
needle_arrays, needle_names = get_needles(paths)

#* Grabbing the screen dimensions
screen_location = get_window_dimensions()
loop_time = time()
while True:
    img = pyautogui.screenshot(region=screen_location)
    haystack_arr = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    bounding_boxes = get_bounding_boxes(haystack_arr, needle_arrays, needle_names)
    detections = show_bounding_boxes(haystack_arr, bounding_boxes, needle_arrays, needle_names)
    cv.imshow('Detections', detections)
    print('FPS', 1/(time() - loop_time))
    loop_time = time()
    if cv.waitKey(1) == ord('q'):
        break

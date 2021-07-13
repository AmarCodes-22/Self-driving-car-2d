import os
import time
from typing import final
import cv2 as cv
from Xlib import display, X
from PIL import Image
import numpy as np
from pprint import pprint
import pyautogui
from object_detection import get_needles, get_bounding_boxes, non_max_supression, show_bounding_boxes
from window_capture import get_window_dimensions
from navigation import calc_distance, navigate


IMAGES_PATH = os.path.join(os.getcwd(), 'data')

gray_paths = {
    'mine_needle': os.path.join(IMAGES_PATH, 'gray_needles', 'mine1.jpg'),
    'yellow_car_smooth_needle': os.path.join(IMAGES_PATH, 'gray_needles', 'yellow-car-smooth.jpg'),
    'yellow_car_edge_needle': os.path.join(IMAGES_PATH, 'gray_needles', 'yellow-car-edge.jpg'),
    'blue_car_smooth_needle': os.path.join(IMAGES_PATH, 'gray_needles', 'blue-car-smooth.jpg'),
    'blue_car_edge_needle': os.path.join(IMAGES_PATH, 'gray_needles', 'blue-car-edge.jpg'),
    'red_car_smooth_needle': os.path.join(IMAGES_PATH, 'gray_needles', 'red-car-smooth.jpg'),
    'red_car_edge_needle': os.path.join(IMAGES_PATH, 'gray_needles', 'red-car-edge.jpg'),
    'power1_needle': os.path.join(IMAGES_PATH, 'gray_needles', 'power1.jpg'),
    'red_truck1_needle': os.path.join(IMAGES_PATH, 'gray_needles', 'red-truck1.jpg'),
    'yellow_truck1_needle': os.path.join(IMAGES_PATH, 'gray_needles', 'yellow-truck1.jpg')
}

#* Defining needles
needle_arrays, needle_names = get_needles(gray_paths)

#* Grabbing the screen dimensions
screen_location = get_window_dimensions()
left_circle_loc, right_circle_loc = (50, 450), (265, 450)
left_tap_location = screen_location[0]+left_circle_loc[0], screen_location[1]+left_circle_loc[1]
right_tap_location = screen_location[0]+right_circle_loc[0], screen_location[1]+right_circle_loc[1]

#* Using Xlib, PIL
TLx, TLy, W,H = screen_location
dsp = display.Display()
root = dsp.screen().root
loop_time = time.time()
count = 0
while True:
    #* Object detection code
    raw = root.get_image(TLx, TLy, W,H, X.ZPixmap, 0xffffffff)
    image = Image.frombytes("RGB", (W, H), raw.data, "raw", "BGRX")
    haystack_arr = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
    cropped_haystack = cv.cvtColor(haystack_arr[175:500, 60:250], cv.COLOR_BGR2GRAY)
    cropped_haystack = np.expand_dims(cropped_haystack, 2)
    rectangles, confs = get_bounding_boxes(cropped_haystack, needle_arrays, needle_names)
    final_rectangles = non_max_supression(rectangles, confs)
    detections = show_bounding_boxes(haystack_arr, final_rectangles)
    
    #* Navigation code
    # distances = calc_distance(final_rectangles)
    # direction = navigate(distances)
    # if direction == -1:
    #     print(len(final_rectangles), 'detections with', direction, 'direction')
    #     pyautogui.click(x=left_tap_location[0], y=left_tap_location[1])
    # elif direction == 1:
    #     print(len(final_rectangles), 'detections with', direction, 'direction')
    #     pyautogui.click(x=right_tap_location[0], y=right_tap_location[1])
    # elif direction == 0:
    #     print(distances)
    # direction = 0

    #* FPS count
    if count % 20 == 0:
        distances = calc_distance(final_rectangles)
        direction = navigate(distances)
        if direction == -1:
            print(len(final_rectangles), 'detection(s) with', direction, 'direction')
            pyautogui.click(x=left_tap_location[0], y=left_tap_location[1])
        elif direction == 1:
            print(len(final_rectangles), 'detection(s) with', direction, 'direction')
            pyautogui.click(x=right_tap_location[0], y=right_tap_location[1])
        elif direction == 0:
            print(distances)
        print('FPS', 1/(time.time()-loop_time))
        count = 0
    loop_time = time.time()
    count += 1

    #* Showing the output
    cv.circle(detections, left_circle_loc, 10, color=(0,0,255), thickness=2)
    cv.circle(detections, right_circle_loc, 10, color=(0,0,255), thickness=2)
    cv.imshow('Detections', detections)
    if cv.waitKey(1) == ord('q'):
        break
    
dsp.close()


#* Debugging
# haystack_arr = cv.imread(os.path.join(IMAGES_PATH, 'haystacks', 'initial_screen.jpg'))
# haystack_arr = cv.resize(haystack_arr, (285, 593))
# cropped_haystack = haystack_arr[175:500, 60:250]
# cropped_haystack = cv.cvtColor(cropped_haystack, cv.COLOR_BGR2GRAY)
# cropped_haystack = np.expand_dims(cropped_haystack, 2)
# rectangles, confs = get_bounding_boxes(cropped_haystack, needle_arrays, needle_names)
# # print(rectangles, confs)
# rectangles = [[70, 274, 32, 45, 2], [72, 274, 32, 45, 2]]
# confs = [0.5, 0.45]
# final_rectangles = non_max_supression(rectangles, confs)
# print('Final', final_rectangles, sep='\n')

# final_haystack = show_bounding_boxes(haystack_arr, final_rectangles)

# distances = calc_distance(final_rectangles)
# # print(distances)

# direction = navigate(distances)
# print(direction)

# cv.circle(final_haystack, (50, 450), 10, color=(0,0,255), thickness=2)
# cv.circle(final_haystack, (265, 450), 10, color=(0,0,255), thickness=2)
# cv.imshow('Final haystack', final_haystack)
# cv.waitKey(0)

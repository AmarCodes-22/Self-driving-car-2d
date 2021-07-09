import os
from time import time
import cv2 as cv
from Xlib import display, X
from PIL import Image
import numpy as np
from pprint import pprint
from object_detection import get_needles, get_bounding_boxes, non_max_supression, show_bounding_boxes
from window_capture import get_window_dimensions


IMAGES_PATH = os.path.join(os.getcwd(), 'data')
paths = {
    'mine_needle': os.path.join(IMAGES_PATH, 'needles', 'mine1.jpg'),
    'yellow_car1_needle': os.path.join(IMAGES_PATH, 'needles', 'yellow-car1.jpg'),
    'yellow_car2_needle': os.path.join(IMAGES_PATH, 'needles', 'yellow-car2.jpg'),
    'blue_car1_needle': os.path.join(IMAGES_PATH, 'needles', 'blue-car1.jpg'),
    'blue_car2_needle': os.path.join(IMAGES_PATH, 'needles', 'blue-car2.jpg'),
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
# print(screen_location)

#* Using Xlib, PIL
TLx, TLy, W,H = screen_location
dsp = display.Display()
root = dsp.screen().root
loop_time = time()
count = 0
while True:
    raw = root.get_image(TLx, TLy, W,H, X.ZPixmap, 0xffffffff)
    image = Image.frombytes("RGB", (W, H), raw.data, "raw", "BGRX")
    haystack_arr = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
    cropped_haystack = haystack_arr[175:500, 60:240]
    rectangles = get_bounding_boxes(cropped_haystack, needle_arrays, needle_names)
    final_rectangles = non_max_supression(rectangles)
    detections = show_bounding_boxes(haystack_arr, final_rectangles)
    if count % 20 == 0:
        print('FPS', 1/(time()-loop_time))
        count = 0
        
    loop_time = time()
    count += 1

    cv.imshow('Detections', detections)
    if cv.waitKey(1) == ord('q'):
        break
    
dsp.close()


#* Debugging
# haystack_arr = cv.imread(os.path.join(IMAGES_PATH, 'haystacks', 'initial_screen.jpg'))
# haystack_arr = cv.resize(haystack_arr, (285, 593))
# cropped_haystack = haystack_arr[175:500, 75:225]
# rectangles = get_bounding_boxes(cropped_haystack, needle_arrays, needle_names)
# final_rectangles = non_max_supression(rectangles)
# for rect in final_rectangles:
#     print(rect)

# print(len(rectangles), len(final_rectangles), final_rectangles)
# cv.imshow('Original haystack', haystack_arr)
# cv.imshow('Cropped', cropped_haystack)

# final_haystack = show_bounding_boxes(haystack_arr, final_rectangles)
# cv.imshow('Final haystack', final_haystack)
# cv.waitKey(0)

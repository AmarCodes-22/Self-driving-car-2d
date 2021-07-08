import os
from time import time
import cv2 as cv
from Xlib import display, X
from PIL import Image
import numpy as np
from pprint import pprint
from object_detection import get_needles, get_bounding_boxes, non_max_supression
from window_capture import get_window_dimensions


IMAGES_PATH = os.path.join(os.getcwd(), 'data')
paths = {
    'mine_needle': os.path.join(IMAGES_PATH, 'needles', 'mine1.jpg'),
    'yellow_car1_needle': os.path.join(IMAGES_PATH, 'needles', 'yellow-car1.jpg'),
    # 'yellow_car2_needle': os.path.join(IMAGES_PATH, 'needles', 'yellow-car2.jpg'),
    # 'blue_car1_needle': os.path.join(IMAGES_PATH, 'needles', 'blue-car1.jpg'),
    # 'red_car1_needle': os.path.join(IMAGES_PATH, 'needles', 'red-car1.jpg'),
    # 'red_car2_needle': os.path.join(IMAGES_PATH, 'needles', 'red-car2.jpg'),
    'power1_needle': os.path.join(IMAGES_PATH, 'needles', 'power1.jpg'),
    # 'red_truck1_needle': os.path.join(IMAGES_PATH, 'needles', 'red-truck1.jpg'),
    'yellow_truck1_needle': os.path.join(IMAGES_PATH, 'needles', 'yellow-truck1.jpg')
}

#* Defining needles
needle_arrays, needle_names = get_needles(paths)

#* Grabbing the screen dimensions
screen_location = get_window_dimensions()
print(screen_location)

# # #* Using Xlib, PIL
TLx, TLy, W,H = screen_location

dsp = display.Display()
root = dsp.screen().root

loop_time = time()
count = 0
while True:
    raw = root.get_image(TLx, TLy, W,H, X.ZPixmap, 0xffffffff)
    image = Image.frombytes("RGB", (W, H), raw.data, "raw", "BGRX")
    # haystack_arr = cv.imread(os.path.join(IMAGES_PATH, 'haystacks', 'initial_screen.jpg'))
    haystack_arr = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
    # cv.imshow('FPS Check', haystack_arr)
    rectangles = get_bounding_boxes(haystack_arr, needle_arrays, needle_names)
    # final_rectangles = non_max_supression(rectangles)
    # bounding_boxes = get_bounding_boxes(haystack_arr, needle_arrays, needle_names)
    # detections = show_bounding_boxes(haystack_arr, bounding_boxes, needle_arrays, needle_names)
    # cv.imshow('Detections', detections)
    if count % 10 == 0:
        print('FPS', 1/(time()-loop_time))
        count = 0
        
    loop_time = time()
    cv.imshow('Output', haystack_arr)
    count += 1
    if cv.waitKey(1) == ord('q'):
        break

dsp.close()


#* Debugging
# haystack_arr = cv.imread(os.path.join(IMAGES_PATH, 'haystacks', 'initial_screen.jpg'))
# haystack_arr = cv.resize(haystack_arr, (285, 593))
# rectangles = get_bounding_boxes(haystack_arr, needle_arrays, needle_names)
# final_rectangles = non_max_supression(rectangles)
# print(len(rectangles), len(final_rectangles))
# cv.imshow('test', haystack_arr)
# cv.waitKey(0)




# print('rectangles', rectangles, sep='\n')
# print('final', final_rectangles, sep='\n')



#* Trying to implement nms from opencv

# bounding_boxes = get_bounding_boxes(haystack_arr, needle_arrays, needle_names)
# bbox = []
# confs = []
# confThreshold = 0
# for i, key in enumerate(bounding_boxes):
#     boxes = bounding_boxes[key]
#     if len(boxes) > 0:
#         for box in boxes:
#             h, w = needle_arrays[i].shape[0], needle_arrays[i].shape[1]
#             x, y = box[0][0], box[0][1]
#             # print('old', box[0][0], box[0][1], needle_h, needle_w)
#             # print('new', box[0][0]+needle_h//2, box[0][1]+needle_w//2, needle_h, needle_w, box[1])
#             bbox.append([x, y, w, h])
#             confs.append(box[1])

# bbox = np.array(bbox)
# print(bbox, len(confs))

# indices = cv.dnn.NMSBoxes(bbox, confs, 0.8, 0.5)
# print(indices)

# pprint(bounding_boxes)
# cv.dnn.NMSBoxes()
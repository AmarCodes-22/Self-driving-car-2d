import os
import cv2 as cv
import pprint
from object_detection import get_needles, get_bounding_boxes, show_bounding_boxes


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

#* defining needles
needle_arrays, needle_names = get_needles(paths)

#* defining haystacks
haystack1_arr = cv.imread(os.path.join(IMAGES_PATH, 'haystacks', '15.jpg'))

#* get bounding boxes
bounding_boxes = get_bounding_boxes(haystack1_arr, needle_arrays, needle_names)
pprint.pprint(bounding_boxes)

#* show bounding boxes
show_bounding_boxes(haystack1_arr, bounding_boxes)

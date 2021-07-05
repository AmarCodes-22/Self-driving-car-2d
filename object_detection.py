import os
import cv2 as cv
import numpy as np

def get_needles(paths:dict):
    '''
    Converts image(s) from local storage to a np array.
    '''
    needle_arrs = []
    needle_names = []
    for i, key in enumerate(paths):
        arr = cv.imread(paths[key])
        needle_arrs.append(arr)
        needle_names.append(paths[key].split('/')[-1])

    return needle_arrs, needle_names

def get_bounding_boxes(haystack: np.ndarray, needles: list, object_names: list):
    '''
    Returns multiple bounding boxes for all object(s). 
    For eg when yellow-car1 exists in multiple positions on screen.
    '''
    bounding_boxes = {}
    len_needles = len(needles)
    threshold = 0.8
    for i in range(len_needles):
        result = cv.matchTemplate(haystack, needles[i], cv.TM_CCOEFF_NORMED)
        (y_cords, x_cords) = np.where(result >= threshold)
        final = []
        for j in range(1, len(y_cords)):
            if (abs(y_cords[j] - y_cords[j-1]) < 10) & (abs(x_cords[j] - x_cords[j-1]) < 10):
                continue
            else:
                print('inside else')
                top_left = (x_cords[j], y_cords[j])
                print(f'shape used for bottom left is from {object_names[i]}')
                bottom_right = (x_cords[j]+needles[i].shape[1], y_cords[j]+needles[i].shape[0])
                final.append(top_left, bottom_right)

        if len(y_cords) >= 1:
            final.append((x_cords[0], y_cords[0]))
            final.append((x_cords[0]+needles[i].shape[1], y_cords[0]+needles[i].shape[0]))

        bounding_boxes[object_names[i]] = final

    return bounding_boxes


def show_bounding_boxes(haystack, bounding_boxes):
    for i, key in enumerate(bounding_boxes):
        if len(bounding_boxes[key]) > 0:
            top_left = bounding_boxes[key][0]
            bottom_right = bounding_boxes[key][1]
            cv.rectangle(haystack, top_left, bottom_right, color=(0,255,0), thickness=2, lineType=cv.LINE_4)

    cv.imshow('Result', haystack)
    cv.waitKey(0)

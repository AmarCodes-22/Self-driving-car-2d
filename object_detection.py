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
        arr = cv.cvtColor(arr, cv.COLOR_BGR2GRAY)
        arr = np.expand_dims(arr, 2)
        needle_arrs.append(arr)
        needle_names.append(paths[key].split('/')[-1])

    return needle_arrs, needle_names


#* Refactored get_bounding_boxes
def get_bounding_boxes(haystack:np.ndarray, needles:list, object_names:list):
    '''
    Returns the bounding boxes for the objects in 
    (top_left_x, top_left_y, bottom_right_x, bottom_right_y, confidence) format
    for all objects whether the object is present or not.
    If the object is not present, the bbox is an empty list.
    '''
    all_rectangles, confs= [],[]
    threshold = 0.7
    for i in range(len(needles)):
        if 'mine' in object_names[i]:
            threshold = 0.5
        else:
            threshold = 0.7

        if 'car' in object_names[i]:
            weight = 1
        elif 'truck' in object_names[i]:
            weight = 2
        else:
            weight = 2

        result = cv.matchTemplate(haystack, needles[i], cv.TM_CCOEFF_NORMED)
        top_lefts = np.where(result >= threshold)
        top_lefts = list(zip(*top_lefts[::-1]))
        if len(top_lefts) > 0:
            h, w = needles[i].shape[0], needles[i].shape[1]
            for top_left in top_lefts:
                confidence = result[top_left[1], top_left[0]]
                all_rectangles.append([top_left[0]+w//2, top_left[1]+h//2, w, h, weight])
                confs.append(confidence)

    return all_rectangles, np.array(confs)

#* Refactoring non_max_supression
def non_max_supression(rectangles:list, confidences:np.ndarray):
    final = []
    sort_args = np.argsort(confidences)[::-1]
    rectangles = np.array(rectangles)[sort_args]
    while len(rectangles) > 0:
        best = rectangles[0]
        mask = np.ones(len(rectangles), dtype=bool)
        final.append(list(best))
        for i in range(len(rectangles)):
            if (abs(rectangles[i][0]-best[0]) < 20) and (abs(rectangles[i][1]-best[1]) < 20):
                mask[i] = False

        rectangles = rectangles[mask]

    return final

#* Refactored show_bounding_boxes
def show_bounding_boxes(haystack:np.ndarray, rectangles:list):
    if len(rectangles) > 1:
        for rect in rectangles:
            shifted_rect = rect[0]+60, rect[1]+175
            w, h = rect[2], rect[3]
            top_left = (shifted_rect[0]-(w//2),shifted_rect[1]-(h//2))
            bottom_right = (top_left[0]+w,top_left[1]+h)
            cv.rectangle(haystack, top_left, bottom_right, (0,255,0), 2, cv.LINE_4)

        return haystack

    return haystack

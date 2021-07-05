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
    threshold = 0.75
    for i in range(len_needles):
        all = []
        result = cv.matchTemplate(haystack, needles[i], cv.TM_CCOEFF_NORMED)
        (y_cords, x_cords) = np.where(result >= threshold)
        
        if len(y_cords) > 0:
            for j in range(len(y_cords)):
                confidence = result[y_cords[j], x_cords[j]]
                all.append(((x_cords[j], y_cords[j]), confidence))

        bounding_boxes[object_names[i]] = all

    return bounding_boxes

def non_max_supression(name:str, boxes:list):
    '''
    Takes in a bunch of bounding boxes and returns the ones that have the highest probability.
    Args:
        boxes list(tuples(tuple, float)):Boxes is a list of boxes. 
                                         Each box is a tuple of its top-left coordinates and confidence.
    '''
    final = []
    final.append(boxes[0])
    for i in range(len(boxes)):
        box_cord, box_conf = boxes[i][0], boxes[i][1]
        # print('final', final)
        if abs(box_cord[0] - final[-1][0][0]) > 10:
            final.append((box_cord, box_conf))
        else:
            if box_conf > final[-1][1]:
                final.pop()
                final.append((box_cord, box_conf))
            else:
                continue

    return final


def show_bounding_boxes(haystack:np.ndarray, bounding_boxes:dict, needles:list, object_names:list):
    supressed = {}
    for i, key in enumerate(bounding_boxes):
        if len(bounding_boxes[key]) > 0:
            supressed_boxes = non_max_supression(key, bounding_boxes[key])
            for box in supressed_boxes:
                box_cord, box_conf = box[0], box[1]
                pos = object_names.index(key)
                
                needle_h = needles[pos].shape[0]
                needle_w = needles[pos].shape[1]
                bottom_right = (box_cord[0]+needle_w, box_cord[1]+needle_h)
                print(object_names[pos], box_cord, bottom_right)

                cv.rectangle(haystack, box_cord, bottom_right, color=(0,255,0), thickness=1, lineType=cv.LINE_4)
                
    cv.imshow('Result', haystack)
    cv.waitKey(0)
                
# In 30.jpg it is still considering a red truck as a yellow truck.
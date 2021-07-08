import os
import cv2 as cv
import numpy as np

def get_needles(paths:dict):
    '''
    Converts image(s) from local storage to a np array.
    '''
    needle_arrs = [] # A list of all needle numpy arrays.
    needle_names = [] # A list of the names inferred from the filenames from the needles folder.
    for i, key in enumerate(paths):
        arr = cv.imread(paths[key])
        needle_arrs.append(arr)
        needle_names.append(paths[key].split('/')[-1])

    return needle_arrs, needle_names


#* Refactored get bounding boxes
def get_bounding_boxes(haystack:np.ndarray, needles:list, object_names:list):
    '''
    Returns the bounding boxes for the objects in (top_left_x, top_left_y, needle_w, needle_h, confidence) format
    for all objects whether the object is present or not. If the obejct is not present, the bbox is an empty list.
    '''
    # bounding_boxes = {}
    all_rectangles = []
    threshold = 0.75
    for i in range(len(needles)):
        # bbox_needle = []
        # locations = []
        result = cv.matchTemplate(haystack, needles[i], cv.TM_CCOEFF_NORMED)
        top_lefts = np.where(result >= threshold)
        top_lefts = list(zip(*top_lefts[::-1]))
        if len(top_lefts) > 0:
            needle_h, needle_w = needles[i].shape[0], needles[i].shape[1]
            for top_left in top_lefts:
                # bottom_right = (top_left[0]+needle_w, top_left[1]+needle_h, result[top_left[1], top_left[0]])
                # locations.append(top_left + bottom_right)
                all_rectangles.append([top_left[0], top_left[1], top_left[0]+needle_w, top_left[1]+needle_h])

    # rectangles, weights = cv.groupRectangles(all_rectangles, 1, 0.5)

        # bounding_boxes[object_names[i]] = locations

    return all_rectangles

#* Refactoring non_max_supression
def non_max_supression(rectangles:list):
    final = []
    if len(rectangles):
        final.append(rectangles[0])
        for i in range(len(rectangles) - 1):
            if abs(rectangles[i][0] - rectangles[i+1][0]) > 10 or abs(rectangles[i][1] - rectangles[i+1][1]) > 10:
                final.append(rectangles[i+1])

        return final



# def non_max_supression(name:str, boxes:list):
#     '''
#     Takes in a bunch of bounding boxes and returns the ones that have the highest probability.
#     Args:
#         boxes list(tuples(tuple, float)):Boxes is a list of boxes. 
#                                          Each box is a tuple of its top-left coordinates and confidence.
#     '''
#     final = []
#     final.append(boxes[0])
#     for i in range(len(boxes)):
#         box_cord, box_conf = boxes[i][0], boxes[i][1]
#         if abs(box_cord[0] - final[-1][0][0]) > 10: # if the objects are not similar add them to the list.
#             final.append((box_cord, box_conf))
#         else: # if they are similar use confidence to decide whether to add or not.
#             if box_conf > final[-1][1]:
#                 final.pop()
#                 final.append((box_cord, box_conf))
#             else:
#                 continue

#     return final


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
                # print(object_names[pos], box_cord, bottom_right)

                cv.rectangle(haystack, box_cord, bottom_right, color=(0,255,0), thickness=1, lineType=cv.LINE_4)
                
    return haystack
    # cv.imshow('Result', haystack)
    # cv.waitKey(1)


# def get_bounding_boxes(haystack: np.ndarray, needles: list, object_names: list):
#     '''
#     Returns multiple bounding boxes for all object(s). 
#     For eg when yellow-car1 exists in multiple positions on screen.
#     '''
#     bounding_boxes = {} # A dict of the object names and their bounding boxes.
#     threshold = 0.7
#     for i in range(len(needles)):
#         if 'truck' in object_names[i]:
#             threshold = 0.8
#         all = []
#         result = cv.matchTemplate(haystack, needles[i], cv.TM_CCOEFF_NORMED)
#         (y_cords, x_cords) = np.where(result >= threshold)
        
#         if len(y_cords) > 0:
#             for j in range(len(y_cords)):
#                 confidence = result[y_cords[j], x_cords[j]]
#                 all.append(((x_cords[j], y_cords[j]), confidence))

#         bounding_boxes[object_names[i]] = all

#     return bounding_boxes

# Can't distinguish between color of the trucks and non max supression doesn't work
# because it only works on boxes for a single object at a time.
# Add more images for yellow car 1 or crop it to remove the effect of the white lines.
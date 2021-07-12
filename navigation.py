# Gets the bounding boxes from main.py and does everything regarding to navigation of the car.
# Current concept:
# 1. Send out rays from the car exactly in front, at 30 degrees to the front on both sides and at 60 degrees
# to the front and 90 degrees to the front on both sides.
# 2. Calculate the distance ie the length of these lines, if any line is obstructed by a bounding box, 
# use it as the border else use x=70, x=230 as the border on left and right respectively.

# New concept: simpler Just get the centre of all the bounding boxes that are present(mine, all others)
# Find the distance between mine and the other boxes from 3 positions, current, 10 pixels to the left and right.
# If the position to the right or left is less than the current go there, instead stay here.

import numpy as np

def find_mine(rectangles:list):
    '''
    Finds the rectange that belongs to our car based on the width and hieght of the needle.
    '''
    found = False
    idx = None
    for i in range(len(rectangles)):
        if rectangles[i][2] == 32 and rectangles[i][3] == 45:
            found = True
            idx = i
            break
    
    return idx

def get_centers(rectangles:list):
    '''
    Iterates all the rectangles and finds their centers.
    '''
    centers = []
    for rect in rectangles:
        center_x = rect[0]+(rect[2])//2
        center_y = rect[1]+(rect[3])//2
        centers.append((center_x, center_y, rect[-1]))

    return centers

# TODO: Add fucntionality to use weights of different objects
def calc_distance(centers:list, index:int):
    '''
    Calculates the distance of out car from other cars and borders.
    '''
    try:
        mine_center = centers[index]
        total_dist, total_dist_left, total_dist_right = 0,0,0
        border_left_dist, border_right_dist = (abs(60-mine_center[0]) ** 2), (abs(250-mine_center[0]) ** 2)
        for i in range(len(centers)):
            print(centers[i][-1])
            p1, p2 = np.array(centers[i]), np.array(mine_center)
            left, right = p2+10, p2-10

            temp = p1 - p2
            temp_left = p1-left
            temp_right = p1-right

            dist = np.dot(temp.T, temp) 
            dist_left = np.dot(temp_left.T, temp_left)
            dist_right = np.dot(temp_right.T, temp_right)

            total_dist += dist
            total_dist_left += dist_left
            total_dist_right += dist_right

        total_dist += (border_left_dist + border_right_dist)
        total_dist_left += (border_left_dist + border_right_dist)
        total_dist_right += (border_left_dist + border_right_dist)

        return (total_dist, total_dist_left, total_dist_right)
    except:
        pass


def navigate(distances:tuple):
    '''
    Makes a decision based on the distance calculated in calc_distance function
    '''
    try:
        dist_curr, dist_left, dist_right = distances[0], distances[1], distances[2]
        right_is_better = False
        left_is_better = False
        if dist_right > dist_curr:
            right_is_better = True
        elif dist_left > dist_curr:
            left_is_better = True

        if right_is_better:
            return 1
        elif left_is_better:
            return -1
        else:
            return 0
    except:
        pass

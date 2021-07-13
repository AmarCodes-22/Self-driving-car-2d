# Concept: Just get the centre of all the bounding boxes that are present(mine, all others)
# Find the distance between mine and the other boxes from 3 positions, current, 10 pixels to the left and right.
# If the distance of position to the right or left is more than the current go there, instead stay here.

import numpy as np

#* Refactoring calc_distance to be faster
def calc_distance(rectangles:list):
    '''
    Calculates the distance of our car from other cars and borders.
    '''
    rectangles = np.array(rectangles)
    # if len(rectangles) == 1:
    #     mine = rectangles[np.where((rectangles[:,2] == 32) * (rectangles[:,3] == 45))][:, 0:2]
    #     if mine[:,0] < 150:
    #         return (0,0,1)
    #     else:
    #         return (0,1,0)
        # center_dist = np.sum((mine - [150, int(mine[:,1])])**2, axis=1)
        # return (0,0,0)
    try:
        mine = rectangles[np.where((rectangles[:,2] == 32) * (rectangles[:,3] == 45))][:, 0:2]
        mine_right = mine + [10,0]
        mine_left = mine - [10,0]

        points = rectangles[:,0:2]
        weights = rectangles[:,-1]

        dists = np.dot(weights, np.sum((points - mine)** 2, axis=1))
        dists_right = np.dot(weights, np.sum((points - mine_right)** 2, axis=1))
        dists_left = np.dot(weights, np.sum((points - mine_left)** 2, axis=1))

        center_dist = np.sum((mine - [150, int(mine[:,1])])**2, axis=1)
        if mine[:,0] < 150:
            dists_right += center_dist
        else:
            dists_left += center_dist

        if len(rectangles) == 1:
            return (dists, dists_left, dists_right)

        # print('distance without center_dist', (dists, dists_left, dists_right))

        # dists = dists - int(center_dist)*5
        # dists_left = dists_left - int(center_dist)*5
        # dists_right = dists_right - int(center_dist)*5

        # print('distance with center_dist', (dists, dists_left, dists_right))

        return (dists, dists_left, dists_right)
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

import PIL
from SolidObject import *
import math
import numpy as np


def point_after_rotation(point, center, degrees):
    """
    use for moving string attachment points with obj
    :param point: point to rotate
    :param center: center of rotation
    :param degrees: angle in degrees (ccw)
    :return: rotates a point about center
    """
    angle = degrees * math.pi / 180
    return ((point[1] - center[1]) * math.cos(angle) - (point[0] - center[0]) * math.sin(angle),
            (point[1] - center[1]) * math.sin(angle) + (point[0] - center[0]) * math.cos(angle))


def find_tilt_direction(obj, pivot, linked_objs=[], touching_objs=[]):
    """
    uses SolidObject class
    :param obj: object to pivot
    :param pivot:
    :param linked_objs: objects linked by strings
    :return:
    """
    base_image = PIL.Image.fromarray(obj.base_image)
    pivot_center = pivot
    cur_rotation = obj.rotation
    new_image = base_image.rotate(
        cur_rotation,
        center=pivot_center,
        expand=True
    )
    new_arr = np.array(new_image)
    new_arr[np.nonzero(new_arr)] = 1

    obj_dim = new_arr.shape
    pivot_col = int(round(pivot[1]))
    left_image = new_arr[0:obj_dim[0], 0:pivot_col]
    right_image = new_arr[0:obj_dim[0], pivot_col:obj_dim[1]]

    total_area = np.count_nonzero(new_arr)
    left_area = np.count_nonzero(left_image)
    right_area = np.count_nonzero(right_image)

    left_right_seperation = obj.coords[1] + pivot[1]
    left_objs = []
    right_objs = []
    """
    # add for objects attached with strings (still pseudocode)
    for o in linked_objs:
        if o.link_pos.x < pivot_center:
            left_objs.append(obj)
        elif o.link_pos.x > pivot_center:
            right_objs.append(obj)
    """
    for o in touching_objs:
        o = o[0] #get the object, not the direction touching
        check = o.coords+np.asarray(o.center)
        if check[1] < left_right_seperation:
            left_objs.append(o)
        elif check[1] > left_right_seperation:
            right_objs.append(o)

    left_area += sum([o.area for o in left_objs])
    right_area += sum([o.area for o in right_objs])

    print("LR other objs", len(left_objs), len(right_objs))
    print("shapes:", obj_dim, left_image.shape, right_image.shape)
    print("TLR:", total_area, left_area, right_area)

    buffer_val = 150
    if left_area > right_area + buffer_val:
        return 1
    elif left_area + buffer_val < right_area:
        return -1
    else:
        return 0


def pivot_object(object, pivot, linked_objects=[], touching_objs=[]):
    pivot_center = pivot
    cur_rotation = object.rotation
    new_rotation = cur_rotation + find_tilt_direction(object, pivot, linked_objects, touching_objs)
    if(new_rotation != cur_rotation):
        objectMoved = False
    else:
        objectMoved = True
    # doesn't actually work
    new_coords = point_after_rotation((0, 0), pivot, new_rotation)
    new_pivot = point_after_rotation(pivot, pivot, new_rotation)

    return new_coords, new_pivot, new_rotation, objectMoved


if __name__ == "__main__":
    pass

import PIL
from SolidObject_pivot import *
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


def find_tilt_direction(obj, pivot, linked_objs=[]):
    """
    uses SolidObject class
    :param obj: object to pivot
    :param pivot:
    :param linked_objs: objects linked by strings
    :return:
    """
    """
    pseudocode
    pivot_center = pivot.center
    left = obj[left:pivot_center]
    right = obj[pivot_center:right]
    left_objs = []
    right_objs = []
    for o in linked_objs:
        if o.link_pos.x < pivot_center:
            left_objs.append(obj)
        elif o.link_pos.x > pivot_center:
            right_objs.append(obj)

    if left_area > right_area:
        return 1
    elif left_area < right_area:
        return -1
    else:
        return 0
    """
    # pivot_center = (obj.coords[0] + pivot[0], obj.coords[1] + pivot[1])
    obj_dim = obj.image.shape
    left_right_seperation = obj.coords[1] - int(round(pivot[1]))
    left_image = obj.image[0:obj_dim[0]][0:left_right_seperation]
    right_image = obj.image[0:obj_dim[0]][left_right_seperation:obj_dim[0]]

    """
    left_objs = []
    right_objs = []
    for o in linked_objs:
        if o.link_pos.x < pivot_center:
            left_objs.append(obj)
        elif o.link_pos.x > pivot_center:
            right_objs.append(obj)
    """
    left_area = np.count_nonzero(left_image)
    right_area = np.count_nonzero(right_image)
    print(left_area, right_area)
    if left_area > right_area:
        return 1
    elif left_area < right_area:
        return -1
    else:
        return 0


def pivot_object(object, pivot, linked_objects=[]):
    """
    pseudocode

    pivot_center = pivot.center
    cur_rotation = obj.rotation

    new_image = object.base_image.rotate(
        cur_rotation+find_tilt_direction(object, pivot, linked_objects),
        center=pivot_center
    )


    return new_image
    """
    base_image = PIL.Image.fromarray(object.base_image)
    # print(object.image)
    pivot_center = pivot
    cur_rotation = object.rotation
    new_rotation = cur_rotation + find_tilt_direction(object, pivot, linked_objects)

    new_image = base_image.rotate(
        new_rotation,
        center=pivot_center,
        expand=True
    )

    new_coords = []
    new_center = []
    new_arr = np.array(new_image)
    new_arr[np.nonzero(new_arr)] = 1

    # crop after rotation with expansion
    coords = np.argwhere(new_arr > 0)
    x0, y0 = coords.min(axis=0)
    x1, y1 = coords.max(axis=0)
    cropped = new_arr[x0:x1+1, y0:y1+1]

    return cropped, new_rotation


if __name__ == "__main__":
    pass

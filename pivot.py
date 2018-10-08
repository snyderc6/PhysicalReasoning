from PIL import Image
from SolidObject import *
import math


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


def find_tilt_direction(obj, pivot, linked_objs):
    """
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
    pass


def pivot_object(object, pivot, linked_objects):
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
    pass


if __name__ == "__main__":
    pass

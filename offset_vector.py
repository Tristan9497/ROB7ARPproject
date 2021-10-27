import math
import numpy as np


def moment(intensity_matrix, p, q):
    """
    :param intensity_matrix: numpy ndarray - input patch
    :param p: int - x coordinate flag
    :param q: int - y coordinate flag
    :return m: float - calculated moment

    Calculates moment as defined in ORB paper and ORB paper ref. 22.
    """
    radius = np.shape(intensity_matrix)[0]//2
    m = 0
    for y in range(radius, -radius-1, -1):
        for x in range(-radius, radius + 1):
            m += x**p * y**q * intensity_matrix[radius-y, radius+x]
    return m


def offset_vector(intensity_matrix):
    """
    :param intensity_matrix: numpy ndarray - input patch
    :return C: numpy ndarray - calculated centroid
    :return theta: float - orientation of patch

    Calculates offset vector as defined in ORB paper and ORB paper ref. 22.
    """
    m00 = moment(intensity_matrix, 0, 0)
    m10 = moment(intensity_matrix, 1, 0)
    m01 = moment(intensity_matrix, 0, 1)
    C = np.array([m10/m00, m01/m00])
    theta = math.atan2(m01, m10)
    return C, theta


if __name__ == '__main__':
    I = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    C, theta = offset_vector(I)
    print(C)
    print(theta)

# # Takes as input the monochrome image, threshold of brightness and outputs FAST features detected as an array of
# something Hardcoded to be FAST-9 #

from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import os


# Takes as input a central pixel value, cardinal pixel values, threshold and outputs the judgement as a boolean
def fast_test_preliminary(pixels, threshold):
    it_is_brighter = True
    it_is_darker = True
    counter_b = 0
    counter_d = 0
    for Intensity in range(len(pixels[1:])):
        if pixels[0] + threshold >= pixels[Intensity + 1]:
            counter_b += 1
            if counter_b == 2:
                it_is_brighter = False
        if pixels[0] - threshold <= pixels[Intensity + 1]:
            counter_d += 1
            if counter_d == 2:
                it_is_darker = False
    return it_is_brighter or it_is_darker


def fast_check_every_preliminary(monoc_image, threshold):
    candidates = []
    for i in range(monoc_image.shape[0]-6):
        for j in range(monoc_image.shape[1]-6):
            pixels = [monoc_image[i+3, j+3],
                      monoc_image[i+3, j+6],
                      monoc_image[i+6, j+3],
                      monoc_image[i, j+3],
                      monoc_image[i+3, j]]
            if fast_test_preliminary(pixels, threshold):
                candidates.append([j, i])
    return candidates


def fast_get_conti_pixels(monoc_image, candidate):
    values = [monoc_image[candidate[0] + 3, candidate[1]],
              monoc_image[candidate[0] + 4, candidate[1]],
              monoc_image[candidate[0] + 5, candidate[1]] + 1,
              monoc_image[candidate[0] + 6, candidate[1]] + 2,
              monoc_image[candidate[0] + 6, candidate[1]] + 3,
              monoc_image[candidate[0] + 6, candidate[1]] + 4,
              monoc_image[candidate[0] + 5, candidate[1]] + 5,
              monoc_image[candidate[0] + 4, candidate[1]] + 6,
              monoc_image[candidate[0] + 3, candidate[1]] + 6,
              monoc_image[candidate[0] + 2, candidate[1]] + 6,
              monoc_image[candidate[0] + 1, candidate[1]] + 5,
              monoc_image[candidate[0], candidate[1]] + 4,
              monoc_image[candidate[0], candidate[1]] + 3,
              monoc_image[candidate[0], candidate[1]] + 2,
              monoc_image[candidate[0] + 1, candidate[1]] + 1,
              monoc_image[candidate[0] + 2, candidate[1]],
              ]
    return values


def fast_end_to_end(monoc_image, threshold):
    cadidate_locations = fast_check_every_preliminary(monoc_image, threshold)
    features_detected_end = []
    return features_detected_end


#pic = cv.imread('/home/thekinga/University/Polybot/TestMap_cropped.jpg')
pic = cv.imread('/home/thekinga/University/PycharmProjects/ROB7ARPproject/aau-city-1.jpg')
monochrome = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
candidate_locations = fast_check_every_preliminary(monochrome, 25)
for i in range(len(candidate_locations)):
    cv.circle(pic, candidate_locations[i], 3, (0), 1)
#features_detected_after_fast = fast_end_to_end(monochrome, 25)
cv.namedWindow('test')
cv.imshow('test', pic)
cv.waitKey()

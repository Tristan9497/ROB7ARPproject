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


# apply the quicktest to every pixel in the input image with threshold, output candidates
def fast_check_every_preliminary(monoc_image, threshold):
    candidates = []
    for i in range(monoc_image.shape[0] - 6):
        for j in range(monoc_image.shape[1] - 6):
            pixels = [monoc_image[i + 3, j + 3],
                      monoc_image[i + 3, j + 6],
                      monoc_image[i + 6, j + 3],
                      monoc_image[i, j + 3],
                      monoc_image[i + 3, j]]
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


# takes as input the pixel values of the circle (+ center), threshold and outputs boolean regarding candidacy
def fast_check_continous_9(center_value, pixel_values, threshold):
    list_of_pixel_values = pixel_values
    bright_or_dark = []
    judgement = False
    for i in range(len(list_of_pixel_values)):
        temp_value = list_of_pixel_values[i]
        if temp_value >= center_value + threshold:
            bright_or_dark += 'b'
        elif temp_value <= center_value - threshold:
            bright_or_dark += 'd'
        else:
            bright_or_dark += 's'
    for i in range(len(list_of_pixel_values)):
        for bds in bright_or_dark:
            if list_of_pixel_values[0:9] == 'b' or list_of_pixel_values[0:9] == 'b':
                judgement = True
                break
            bright_or_dark.append(bright_or_dark.pop(0))
    return judgement


def fast_end_to_end(monoc_image, threshold):
    cadidate_locations = fast_check_every_preliminary(monoc_image, threshold)
    features_detected_end = []
    return features_detected_end


# pic = cv.imread('/home/thekinga/University/Polybot/TestMap_cropped.jpg')
# pic = cv.imread('/home/thekinga/University/PycharmProjects/ROB7ARPproject/aau-city-1.jpg')
# monochrome = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
# candidate_locations = fast_check_every_preliminary(monochrome, 25)
# for i in range(len(candidate_locations)):
#     cv.circle(pic, candidate_locations[i], 3, (0), 1)
# # features_detected_after_fast = fast_end_to_end(monochrome, 25)
# cv.namedWindow('test')
# cv.imshow('test', pic)
# cv.waitKey()

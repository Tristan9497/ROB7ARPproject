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


def fast_end_to_end(monoc_image, threshold):
    cv.namedWindow('test')
    cv.imshow('test', monoc_image)
    for i in range(monoc_image.shape[0]):
        for j in range(monoc_image.shape[1]):
            pass

    features_detected_end = []
    return features_detected_end


pic = cv.imread('/home/thekinga/University/Polybot/TestMap_cropped.jpg')
monochrome = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
features_detected_after_fast = fast_end_to_end(monochrome, 25)
cv.waitKey()

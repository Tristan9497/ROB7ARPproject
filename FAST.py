# # Takes as input the monochrome image, threshold of brightness and outputs FAST features detected as an array of
# something Hardcoded to be FAST-9 #

from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import os


class Detector:
    def __init__(self, n=9, threshold=25):
        if not 8 < n < 16:
            print(n, " is not a valid parameter, expect errors")
        self.n = n
        self.threshold = threshold
        self.bright_array_n = []
        self.dark_array_n = []
        for i in range(n):
            self.bright_array_n += 'b'
            self.dark_array_n += 'd'

    # Takes as input a central pixel value, cardinal pixel values, threshold and outputs the judgement as a boolean
    def test_preliminary(self, pixels):
        it_is_brighter = True
        it_is_darker = True
        counter_b = 0
        counter_d = 0
        for Intensity in range(len(pixels[1:])):
            if pixels[0] + self.threshold >= pixels[Intensity + 1]:
                counter_b += 1
                if counter_b == 2:
                    it_is_brighter = False
            if pixels[0] - self.threshold <= pixels[Intensity + 1]:
                counter_d += 1
                if counter_d == 2:
                    it_is_darker = False
        return it_is_brighter or it_is_darker

    # apply the quicktest to every pixel in the input image with threshold, output candidates as pixel coordinate of
    # upper left corner
    def check_every_preliminary(self, monoc_image):
        candidates = []
        for i in range(monoc_image.shape[0] - 7):
            for j in range(monoc_image.shape[1] - 7):
                pixels = [monoc_image[i + 3, j + 3],
                          monoc_image[i + 3, j + 6],
                          monoc_image[i + 6, j + 3],
                          monoc_image[i, j + 3],
                          monoc_image[i + 3, j]]
                if Detector.test_preliminary(self, pixels):
                    candidates.append([j, i])
        return candidates

    def get_conti_pixels(self, monoc_image, candidate):
        print(candidate)
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
    def check_continous(self, center_value, pixel_values):
        bright_or_dark = []
        judgement = False
        for i in range(len(pixel_values)):
            temp_value = pixel_values[i]
            if temp_value >= center_value + self.threshold:
                bright_or_dark += 'b'
            elif temp_value <= center_value - self.threshold:
                bright_or_dark += 'd'
            else:
                bright_or_dark += 's'
        for i in range(len(pixel_values)):
            # print(bright_or_dark, judgement)
            if bright_or_dark[0:self.n] == self.bright_array_n or bright_or_dark[0:self.n] == self.dark_array_n:
                judgement = True
                break
            bright_or_dark.append(bright_or_dark.pop(0))
        return judgement

    def end_to_end(self, monoc_image):
        features_detected_end = []
        candidate_locations = Detector.check_every_preliminary(self, monoc_image)
        for candidate in candidate_locations:
            pixel_values_around_candidate = Detector.get_conti_pixels(self, monoc_image, candidate)
            Detector.check_continous(self, monoc_image[candidate[0] + 3, candidate[1] + 3],
                                     pixel_values_around_candidate)
            features_detected_end += candidate
        return features_detected_end


# pic = cv.imread('/home/thekinga/University/Polybot/TestMap_cropped.jpg')
fast_detector = Detector()
pic = cv.imread('/home/thekinga/University/PycharmProjects/ROB7ARPproject/aau-city-1.jpg')
monochrome = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
candidate_locations = fast_detector.end_to_end(monochrome)
for index in range(len(candidate_locations)):
    cv.circle(pic, candidate_locations[index], 3, (0), 1)
# features_detected_after_fast = fast_end_to_end(monochrome, 25)
cv.namedWindow('test')
cv.imshow('test', pic)
cv.waitKey()

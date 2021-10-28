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
                    candidates.append([i, j])
        return candidates

    def get_conti_pixels(self, monoc_image, candidate):
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

    def nms(self, candidate_coordinates, overlap_thresh=0.4):
        # Return an empty list, if no boxes given
        if len(candidate_coordinates) == 0:
            return []
        x1 = candidate_coordinates[:, 0]  # x coordinate of the top-left corner
        y1 = candidate_coordinates[:, 1]  # y coordinate of the top-left corner
        x2 = candidate_coordinates[:, 0]  # x coordinate of the bottom-right corner
        y2 = candidate_coordinates[:, 1]  # y coordinate of the bottom-right corner
        # Compute the area of the bounding boxes and sort the bounding
        # Boxes by the bottom-right y-coordinate of the bounding box
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)  # We add 1, because the pixel at the start as well as at the end counts
        # The indices of all boxes at start. We will redundant indices one by one.
        indices = np.arange(len(x1))
        for i, box in enumerate(candidate_coordinates):
            # Create temporary indices
            temp_indices = indices[indices != i]
            # Find out the coordinates of the intersection box
            xx1 = np.maximum(box[0], candidate_coordinates[temp_indices, 0])
            yy1 = np.maximum(box[1], candidate_coordinates[temp_indices, 1])
            xx2 = np.minimum(box[2], candidate_coordinates[temp_indices, 2])
            yy2 = np.minimum(box[3], candidate_coordinates[temp_indices, 3])
            # Find out the width and the height of the intersection box
            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)
            # compute the ratio of overlap
            overlap = (w * h) / areas[temp_indices]
            # if the actual bounding box has an overlap bigger than treshold with any other box, remove it's index
            if np.any(overlap) > overlap_thresh:
                indices = indices[indices != i]
        # return only the boxes at the remaining indices
        return candidate_coordinates[indices].astype(int)

    def end_to_end_on_single(self, monoc_image):
        features_detected_end = []
        candidate_locations = Detector.check_every_preliminary(self, monoc_image)
        for candidate in candidate_locations:
            pixel_values_around_candidate = Detector.get_conti_pixels(self, monoc_image, candidate)
            if Detector.check_continous(self, monoc_image[candidate[0] + 3, candidate[1] + 3],
                                        pixel_values_around_candidate):
                features_detected_end += [candidate]
        return features_detected_end

    def end_to_end(self, monoc_image_pyramid):
        features_detected_end = []
        scale = 1
        for monoc_image in monoc_image_pyramid:
            print("starting on a new level")
            features_detected = Detector.end_to_end_on_single(self, monoc_image)
            features_detected_nms = np.hstack([np.array(features_detected), np.add(np.array(features_detected), 6)])
            features_detected_nms = Detector.nms(self, features_detected_nms)[:, :2]
            # print(features_detected_nms.shape)
            features_detected_end.extend(np.multiply(features_detected_nms, scale))
            scale *= 2
        return features_detected_end


# pic = cv.imread('/home/thekinga/University/Polybot/TestMap_cropped.jpg')

n = 9
t = 30

fast_detector = Detector(n, t)
pic = cv.imread('/home/thekinga/University/PycharmProjects/ROB7ARPproject/aau-city-1.jpg')
pic2 = cv.imread('/home/thekinga/University/PycharmProjects/ROB7ARPproject/aau-city-1.jpg')
monochrome = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
s_rows, s_cols = map(int, monochrome.shape)
# print(s_cols, s_rows)
monoc_image_pyramid = []
monoc_image_pyramid += [monochrome]
monoc_image_pyramid += [cv.pyrDown(monochrome)]
monoc_image_pyramid += [cv.pyrDown(monoc_image_pyramid[1])]
monoc_image_pyramid += [cv.pyrDown(monoc_image_pyramid[2])]
# print(len(monoc_image_pyramid))
final_detections = fast_detector.end_to_end(monoc_image_pyramid)
# print(len(final_detections))
for index in range(len(final_detections)):
    cv.circle(pic, [final_detections[index][1], final_detections[index][0]], 5, (0), 1)
cv.namedWindow('test')
cv.imshow('test', pic)

cv.waitKey()

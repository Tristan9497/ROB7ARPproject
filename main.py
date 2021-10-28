
from FAST import *
from brief import *
from offset_vector import *

"""
main file skeleton that probably does not work
"""

# TODO add output previews if not added in functions themselves already

image_location = "./test.jpg"
image_location=r'/Users/tristan/OneDrive - Aalborg Universitet/Aalborg University/Semester1/Perception/Exercises/aau-city-1.jpg'

pic = cv2.imread(image_location)
monochrome = cv.cvtColor(pic, cv2.COLOR_BGR2GRAY)

fast_detector = Detector()
patches = fast_detector.end_to_end(monochrome)

brief(image_location,patches,31)


# # TODO check if logic is correct
# harris_measures = np.ndarray()
# for patch in patches:
#     patch = np.float32(patch)
#     patch_harris_values = cv2.cornerHarris(patch, 2, 3, 0.04) # TODO check params
#     np.append(harris_measures, np.sum(patch_harris_values))
#
# N_patches = 100
# ind = np.argpartition(harris_measures, -N_patches)[-N_patches:]
#
# patches = patches[ind]
#
# descriptors = np.ndarray()
# for patch in patches:
#     C, theta = offset_vector(patch)
#     patch_descriptors = brief(patch, theta)
#     descriptors = np.vstack([descriptors, patch_descriptors])







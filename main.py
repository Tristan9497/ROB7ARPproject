
from FAST import *
from brief import *
from offset_vector import *
import matplotlib as plt

"""
main file skeleton that probably does not work
"""

# TODO add output previews if not added in functions themselves already

image_location = "./test.jpg"
image_location=r'/Users/tristan/OneDrive - Aalborg Universitet/Aalborg University/Semester1/Perception/Exercises/aau-city-1.jpg'
image_location2=r'/Users/tristan/OneDrive - Aalborg Universitet/Aalborg University/Semester1/Perception/Exercises/aau-city-2.jpg'
img1 = cv2.imread(image_location)
img2 = cv2.imread(image_location2)
monochrome = cv.cvtColor(img1, cv2.COLOR_BGR2GRAY)
monochrome2 = cv.cvtColor(img2, cv2.COLOR_BGR2GRAY)

fast_detector = Detector()
patches = fast_detector.end_to_end(monochrome)
patches2 = fast_detector.end_to_end(monochrome2)

des1=brief(monochrome,patches,31)
des2=brief(monochrome2,patches2,31)
##Matcher

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1,des2)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3 = cv2.drawMatches(img1,patches,img2,patches2,matches[:10], flags=2)
plt.imshow(img3),plt.show()
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







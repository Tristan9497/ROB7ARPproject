
from FAST import *
from brief import *
from offset_vector import *
import matplotlib as plt


def generateimagepyramid(monochrome_input, k=3):
    monoc_image_pyramid = []
    monoc_image_pyramid += [monochrome_input]
    if k >= 2:
        monoc_image_pyramid += [cv.pyrDown(monochrome_input)]
    if k >= 3:
        monoc_image_pyramid += [cv.pyrDown(monoc_image_pyramid[1])]
    if k >= 4:
        monoc_image_pyramid += [cv.pyrDown(monoc_image_pyramid[2])]
    return monoc_image_pyramid


# TODO add output previews if not added in functions themselves already

# image_location = "./test.jpg"
image_location = r'/Users/tristan/OneDrive - Aalborg Universitet/Aalborg University/Semester1/Perception/Exercises/aau-city-1.jpg'
image_location2 = r'/Users/tristan/OneDrive - Aalborg Universitet/Aalborg University/Semester1/Perception/Exercises/aau-city-2.jpg'
#image_location = r'/home/thekinga/University/PycharmProjects/ROB7ARPproject/aau-city-1.jpg'
#image_location2 = r'/home/thekinga/University/PycharmProjects/ROB7ARPproject/aau-city-2.jpg'

img1 = cv2.imread(image_location)
img2 = cv2.imread(image_location2)
monochrome = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
monochrome2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

fast_detector = Detector()
patches = fast_detector.end_to_end(generateimagepyramid(monochrome))
patches2 = fast_detector.end_to_end(generateimagepyramid(monochrome2))

des1 = brief(monochrome, patches, 31)
des2 = brief(monochrome2, patches2, 31)

# orb = cv2.ORB_create()

# Matcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1, des2)

# Sort them in the order of their distance.
matches = sorted(matches, key=lambda x: x.distance)
patches = np.array(patches)
patches2 = np.array(patches2)
img3 = np.array([])
# Draw first 10 matches.
ORB_matches = cv2.drawMatches(img1, patches, img2, patches2, matches[:], None, flags=2)
cv2.imshow(ORB_matches)

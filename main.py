
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

# image_location = "./test.jpg"
image_location = r'/Users/tristan/OneDrive - Aalborg Universitet/Aalborg University/Semester1/Perception/Exercises/aau-city-1.jpg'
image_location2 = r'/Users/tristan/OneDrive - Aalborg Universitet/Aalborg University/Semester1/Perception/Exercises/aau-city-2.jpg'
#image_location = r'/home/thekinga/University/PycharmProjects/ROB7ARPproject/aau-city-1.jpg'
#image_location2 = r'/home/thekinga/University/PycharmProjects/ROB7ARPproject/aau-city-2.jpg'
if __name__=="__main__":
    img1 = cv2.imread(image_location)
    img2 = cv2.imread(image_location2)
    monochrome = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    monochrome2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    fast_detector = Detector()
    patches = fast_detector.end_to_end(generateimagepyramid(monochrome))
    patches2 = fast_detector.end_to_end(generateimagepyramid(monochrome2))

    kp1, des1 = brief(monochrome, patches, 31)
    kp2, des2 = brief(monochrome2, patches2, 31)

    # Matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)

    # Draw first 10 matches.
    ORB_matches =cv2.drawMatches(img1, kp1, img2, kp2, matches[:], None, flags=2)
    cv2.imshow('Matches', ORB_matches)


    # for index in range(len(patches)):
    #      cv2.circle(img1, [patches[index][1] + 3, patches[index][0] + 3], 5, (0, 0, 255), 1)
    # cv2.namedWindow('test2')
    # cv2.imshow("test2",img1)
    #
    #
    # for index in range(len(patches2)):
    #     cv2.circle(img2, [patches2[index][1] + 3, patches2[index][0] + 3], 5, (0, 0, 255), 1)
    # cv2.namedWindow('test3')
    # cv2.imshow("test3", img2)


    cv2.waitKey(0)


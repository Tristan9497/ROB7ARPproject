from FAST import *
from brief import *
from offset_vector import *
import matplotlib.pyplot as plt


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
image_location = r'/Users/tristan/Desktop/Neuer Ordner/aau-city-1.jpg'
image_location2 = r'/Users/tristan/Desktop/Neuer Ordner/aau-city-2rot.jpg'
# image_location = r'/home/thekinga/University/PycharmProjects/ROB7ARPproject/aau-city-1.jpg'
# image_location2 = r'/home/thekinga/University/PycharmProjects/ROB7ARPproject/aau-city-2.jpg'
if __name__ == "__main__":
    img1 = cv2.imread(image_location)
    img2 = cv2.imread(image_location2)
    monochrome = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    monochrome2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    fast_detector = Detector()
    patches = fast_detector.end_to_end(generateimagepyramid(monochrome))
    patches2 = fast_detector.end_to_end(generateimagepyramid(monochrome2))

    brief_descriptor = rBRIEF(31)
    kp1, des1 = brief_descriptor.brief(monochrome, patches)
    kp2, des2 = brief_descriptor.brief(monochrome2, patches2)

    orb = cv2.ORB_create()

    # find the keypoints with ORB
    orbkp ,orbdes= orb.detectAndCompute(monochrome,None)
    orbkp2, orbdes2 = orb.detectAndCompute(monochrome2, None)


    # compute the descriptors with ORB


    # Match with brute force matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    matches2=bf.match(orbdes,orbdes2)
    matches2= sorted(matches2, key=lambda x: x.distance)
    # Draw matches
    ORB_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, flags=2)
    ORB_matches2 = cv2.drawMatches(img1, orbkp, img2, orbkp2, matches2[:50], None, flags=2)
    cv2.imwrite('/Users/tristan/Desktop/ARP_ORB_matches.jpg', ORB_matches)
    cv2.imwrite('/Users/tristan/Desktop/OPENCV_ORB_matches.jpg', ORB_matches2)
    cv2.imshow('Matches', ORB_matches)
    #plt.imshow(ORB_matches2)
    cv2.imshow('ORBMatches',ORB_matches2)

    cv2.waitKey(0)

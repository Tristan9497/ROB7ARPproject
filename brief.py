import cv2
from offset_vector import *


class rBRIEF:
    def __init__(self, patchw):
        self.patchw = patchw
        # number of 2^n
        self.testnum = 256
        self.X = np.zeros((30, self.testnum, 2))
        self.Y = np.zeros((30, self.testnum, 2))
        self.sigma = (1 / 25) * (self.patchw ** 2)
        self.maxw = np.ceil(self.patchw / 2).astype(int)
        self.patchr = np.floor(self.patchw / 2).astype(int)
        self.createbintestcoordinates()

    def getcoordinate(self):
        # find normaly distributed coordinates in the largest circle
        cov = np.eye(2) * self.sigma
        while True:
            s = np.random.multivariate_normal((0, 0), cov)
            if np.floor(np.sqrt(s[0] ** 2 + s[1] ** 2)) < self.patchr:
                return s

    def createbintestcoordinates(self):
        # generate random coordinates in patch
        for j in range(self.testnum):
            self.X[0, j] = self.getcoordinate()
            self.Y[0, j] = self.getcoordinate()

        # create lookuptable for all 30 rotations
        c, s = np.cos(np.radians(12)), np.sin(np.radians(12))
        R = np.array(((c, -s), (s, c)))
        for i in range(1, 30):
            self.X[i] = np.dot(self.X[i - 1], R.T)
            self.Y[i] = np.dot(self.Y[i - 1], R.T)

    def brief(self, image, kp):
        Descriptors = []
        Keypoints = []
        for i in range(np.shape(kp)[0]):
            x = np.floor(kp[i][1]).astype(int)
            y = np.floor(kp[i][0]).astype(int)

            # check if keypoint is outofbounds then create patch and calc descriptors
            if self.maxw < x < (image.shape[1] - self.maxw) and self.maxw < y < (image.shape[0] - self.maxw):
                # create ROI at kp location
                patch_image = image[y - self.patchr:y + self.maxw, x - self.patchr:x + self.maxw]

                # get orientation of the patch
                theta = offset_vector(patch_image)[1]

                # calculate descriptor for this patch and append it
                Descriptors.append(self.calculateDescriptor(patch_image, theta))
                # convert keypoint to opencv type
                Keypoints.append(cv2.KeyPoint(x.astype(float), y.astype(float), 1, angle=theta))
        return Keypoints, np.array(Descriptors).astype(np.uint8)

    def calculateDescriptor(self, src, theta):
        ##assume theta is in radian already
        img = cv2.GaussianBlur(src, (5, 5), 2, 2, cv2.BORDER_DEFAULT)
        descriptor = []

        # find according binarytests in lookuptable
        rotincrement = int(np.round(theta / np.radians(12)))
        if rotincrement > 30: rotincrement -= 30

        # split uint256 in 32 bytes so bfmatcher can handle it and the output is equal to the opencv function
        for i in range(int(self.testnum / 8)):
            binarystring = 0
            for j in range(8):
                index = i * 8 + j
                # lookup correct coordinate pairs and offset them by the patchradius
                xx = int(np.floor(self.X[rotincrement, index, 0])) + self.patchr
                xy = int(np.floor(self.X[rotincrement, index, 1])) + self.patchr
                yx = int(np.floor(self.Y[rotincrement, index, 0])) + self.patchr
                yy = int(np.floor(self.Y[rotincrement, index, 1])) + self.patchr
                if img[xx, xy] < img[yx, yy]:
                    tao = 1
                else:
                    tao = 0
                binarystring += pow(2, j - 1) * tao
            descriptor.append(binarystring)
        return descriptor

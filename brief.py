import cv2
from offset_vector import *

class rBRIEF:
    def __init__(self, patchw):
        self.patchw = patchw
        self.testnum = 8
        self.X = np.zeros((self.testnum,2))
        self.Y = np.zeros((self.testnum, 2))
        self.sigma = (1 / 25) * (self.patchw ** 2)
        self.maxw = np.ceil(self.patchw / 2).astype(int)
        self.patchr = np.floor(self.patchw / 2).astype(int)
        self.createbintestcoordinates()

    def getcoordinate(self):
        #find normaly distributed coordinates in the largest circle
        cov = np.eye(2)*self.sigma
        while True:
            s = np.random.multivariate_normal((0,0), cov)
            if np.floor(np.sqrt(s[0]**2+s[1]**2))<self.patchr:
                #translate to patch coordinates
                s=[int(np.floor(x)) for x in s]
                return s

    def createbintestcoordinates(self):
        #calculate max pixel distance to prevent out of bounds while turning the testpoints
        for i in range(self.testnum):
            self.X[i] = self.getcoordinate()
            self.Y[i] = self.getcoordinate()


    def brief(self, image, kp):
        Descriptors = []
        Keypoints = []
        for i in range(np.shape(kp)[0]):
            x = np.floor(kp[i][1]).astype(int)
            y = np.floor(kp[i][0]).astype(int)

            #check if keypoint is outofbounds then create patch and calc descriptors
            if self.maxw<x<(image.shape[1]-self.maxw) and self.maxw<y<(image.shape[0]-self.maxw):
                #create ROI at kp location
                patch_image = image[y-self.patchr:y+self.maxw, x-self.patchr:x + self.maxw]

                #get orientation of the patch
                theta=offset_vector(patch_image)[1]

                #calculate descriptor lookuptable for this patch and append it
                Descriptors.append(self.calculateDescriptor(patch_image, theta))
                Keypoints.append(cv2.KeyPoint(x.astype(float), y.astype(float), 1, angle=theta))
        return Keypoints, np.array(Descriptors).astype(np.uint8)

    def calculateDescriptor(self, src, theta):
        ##assume thata is in radian already
        img=cv2.GaussianBlur(src, (9,9), 2, 2, cv2.BORDER_DEFAULT)
        binarystring = 0
        rotdescriptors = []

        #rotate to patch orientation from oFAST
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))

        #create mirror of var for rotating without changing the original
        Xr = np.dot(self.X, R)
        Yr = np.dot(self.Y, R)

        angleoffset = np.radians(12)
        c, s = np.cos(angleoffset), np.sin(angleoffset)
        R = np.array(((c, -s), (s, c)))

        for j in range(30):
            for i in range(self.testnum):
                xx = int(np.floor(Xr[i, 0])) + self.patchr
                xy = int(np.floor(Xr[i, 1])) + self.patchr
                yx = int(np.floor(Yr[i, 0])) + self.patchr
                yy = int(np.floor(Yr[i, 1])) + self.patchr
                if img[xx, xy] < img[yx, yy]:
                    tao = 1
                else:
                    tao = 0
                binarystring += pow(2, i-1)*tao
            #rotate binary test by 12deg according to rBRIEF
            Xr = np.dot(Xr, R)
            Yr = np.dot(Yr, R)
            rotdescriptors.append(binarystring)

        return rotdescriptors


import cv2
import numpy as np
from offset_vector import *
import matplotlib.pyplot as plt

def getcoordinate(mu, sigma, patchw):
    while True:
        s = np.round(np.random.normal(mu, sigma, 1))
        if s >= -np.floor(patchw / 2) and s <= np.floor(patchw / 2):
            return s

def brief(image, kp, patchw):
    Descriptors = []
    Keypoints=[]
    for i in range(np.shape(kp)[0]):
        x = np.floor(kp[i][1]).astype(int)
        y = np.floor(kp[i][0]).astype(int)
        maxw=np.ceil(patchw/2).astype(int)
        patchr=np.floor(patchw/2).astype(int)
        #check if keypoint is outofbounds

        if maxw<x<(image.shape[1]-maxw) and maxw<y<(image.shape[0]-maxw) :

            patch_image = image[y-patchr:y+maxw,x-patchr:x + maxw]


            #call antes function to get theta
            c, theta=offset_vector(patch_image)
            keypoint = cv2.KeyPoint(x.astype(float), y.astype(float), 1, angle=theta)
            descriptor=calculateDescriptor(patch_image,theta)
            Descriptors.append(descriptor)
            Keypoints.append(keypoint)
    Output=np.array(Descriptors)
    Output=Output.astype(np.uint8)
    print(Output)
    return Keypoints, Output

def calculateDescriptor(src, theta):
    ##assume thata is in radian already
    Patchw=src.shape[0]
    sigma =(1/25)*(Patchw**2)
    num = 8
    kernelshape=(9, 9)
    img=cv2.GaussianBlur(src,kernelshape,2,2,cv2.BORDER_DEFAULT)


    binarystring=0
    tao=0
    ##create all coordinates
    X = np.zeros((num,2))
    Y = np.zeros((num,2))
    #calculate max pixel distance to prevent out of bounds while turning the testpoints
    maxdist=np.floor(np.sqrt(0.5*Patchw*Patchw))

    for i in range(num):
        X[i,0] = getcoordinate(0, sigma, maxdist).astype(int)
        X[i,1] = getcoordinate(0, sigma, maxdist).astype(int)
        Y[i,0] = getcoordinate(0, sigma, maxdist).astype(int)
        Y[i,1] = getcoordinate(0, sigma, maxdist).astype(int)
        ##rotate all points by angle of patch

    ##calculate the binarystring
    rlt=[]
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    for j in range(30):


        X = np.dot(X, R)
        Y = np.dot(Y, R)
        angleoffset = np.radians(12)
        c, s = np.cos(angleoffset), np.sin(angleoffset)
        R = np.array(((c, -s), (s, c)))
        for i in range(num):
            xx=np.floor(X[i,0]).astype(int)
            xy=np.floor(X[i,1]).astype(int)
            yx=np.floor(Y[i,0]).astype(int)
            yy=np.floor(Y[i,1]).astype(int)

            if img[xx,xy] < img[yx,yy]:
                tao=1
            else:
                tao=0
            binarystring+=pow(2,i-1)*tao

        #     plt.plot([xx + 15, yx + 15],[xy + 15, yy + 15], color="white", linewidth=1)
        #     plt.scatter([xx + 15],[xy+15],c="b")
        #     plt.scatter([yx + 15], [yy + 15],c="r")
        # plt.title(j)
        # plt.imshow(img, cmap='gray', vmin=0, vmax=255)
        # plt.show()
        rlt.append(binarystring)
    return rlt

if __name__=="__main__":
    #create random patch
    #src=np.random.randint(255, size=(31, 31),dtype=np.uint8)
    src=cv2.imread(r'/Users/tristan/OneDrive - Aalborg Universitet/Aalborg University/Semester1/Perception/Exercises/aau-city-1.jpg')

    src=cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    #creating random keypoints for testing purposes
    kp=np.random.rand(3,10)
    kp[0,:] *= src.shape[1]
    kp[1,:] *= src.shape[0]
    kp[2,:] *= 2*np.pi

    #print(kp)
    brief(src,kp,31)

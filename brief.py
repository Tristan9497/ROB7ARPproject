import cv2
import numpy as np


def getcoordinate(mu, sigma, patchw):
    while True:
        s = np.round(np.random.normal(mu, sigma, 1))
        if s >= -np.floor(patchw / 2) and s <= np.floor(patchw / 2):
            return s

def brief(src, theta):
    ##assume thata is in radian already
    Patchw=src.shape[0]
    sigma =(1/25)*Patchw*Patchw
    num = 128
    kernelshape=(9,9)


    img=cv2.GaussianBlur(src,kernelshape,2,2,cv2.BORDER_DEFAULT)

    binarystring=0
    tao=0

    ##create all coordinates
    X = np.zeros((num,2))
    Y = np.zeros((num,2))
    for i in range(num):
        X[i,0] = getcoordinate(0, sigma, Patchw).astype(int)
        X[i,1] = getcoordinate(0, sigma, Patchw).astype(int)
        Y[i,0] = getcoordinate(0, sigma, Patchw).astype(int)
        Y[i,1] = getcoordinate(0, sigma, Patchw).astype(int)
    ##rotate all points by angle of patch


    ##calculate the binarystring
    rlt=np.zeros(30)
    for j in range(30):
        angleoffset=np.deg2rad(12)

        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))
        theta+=angleoffset
        Xtheta = np.dot(X, R.T)
        Ytheta = np.dot(Y, R.T)
        for i in range(num):
            xx=X[i,0].astype(int)
            xy=X[i,1].astype(int)
            yx=Y[i,0].astype(int)
            yy=Y[i,1].astype(int)
            if src[xx,xy] < src[yx,yy]:
                tao=1
            else:
                tao=0
            binarystring+=pow(2,i-1)*tao
        rlt[j]=binarystring
    return rlt

if __name__=="__main__":
    #create random patch
    src=np.random.randint(255, size=(31, 31),dtype=np.uint8)

    cv2.imshow('random patch', src)
    identifier=brief(src,0)
    cv2.waitKey(0)

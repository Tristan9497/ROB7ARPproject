import cv2
import numpy as np


def getcoordinate(mu, sigma, patchw):
    while True:
        s = np.round(np.random.normal(mu, sigma, 1))
        if s >= -np.floor(patchw / 2) and s <= np.floor(patchw / 2):
            return s

def brief(src):

    Patchw=src.shape[0]
    sigma =(1/25)*Patchw*Patchw
    num = 128
    kernelshape=(9,9)


    img=cv2.GaussianBlur(src,kernelshape,2,2,cv2.BORDER_DEFAULT)
    cv2.imshow('pic', img)
    bitstring=0
    theta=0
    for i in range(num):
        x1 = getcoordinate(0, sigma, Patchw).astype(int)
        y1 = getcoordinate(0, sigma, Patchw).astype(int)
        x2 = getcoordinate(0, sigma, Patchw).astype(int)
        y2 = getcoordinate(0, sigma, Patchw).astype(int)

        if src[x1,y1]<src[x2,y2]:
            theta=1
        else:
            theta=0
        bitstring=pow(2,i-1)*theta

    print(bitstring)
    cv2.waitKey(0)
if __name__=="__main__":
    #create random patch
    src=np.random.randint(255, size=(31, 31),dtype=np.uint8)
    brief(src)

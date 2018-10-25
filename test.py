import cv2 as cv
import numpy as np

imagepath="/home/bobchen/dataset/2012_004283.jpg"


img=cv.imread(imagepath,1)
imgn=np.array(img)
print(imgn.shape)
# imgn[104,:]=(0,0,255)
# imgn[:,169]=(0,0,255)
imgn[31:364,203:327]=(0,0,255)
cv.imshow("showimage",imgn)
cv.waitKey(0)
cv.destroyAllWindows()
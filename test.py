import cv2 as cv
import numpy as np

imagepath="/home/bobchen/annationdist/VOC/OriginalImages/MVI_7392_578.jpg"


img=cv.imread(imagepath,1)
imgn=np.array(img)
print(imgn.shape)
# imgn[104,:]=(0,0,255)
# imgn[:,169]=(0,0,255)
#imgn[98:134,455:489]=(0,0,255)
rates=(1920/871)
imgn[int(98*rates):int(134*rates),int(455*rates):int(489*rates)]=(0,0,255)
cv.imshow("showimage",imgn)
cv.waitKey(0)
cv.destroyAllWindows()
import cv2
import numpy as np

# girelecek foto
image=cv2.imread("kare2.png")

# gerekli filtreleme islemleri
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blur=cv2.medianBlur(gray,5)
sharpen_kernel=np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
sharpen=cv2.filter2D(blur,-1,sharpen_kernel)

# threshold islemi
thresh=cv2.threshold(sharpen,160,255,cv2.THRESH_BINARY_INV)[1]
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
close=cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel,iterations=2)

# threshhold alaninin icinden contour bulma
cnts=cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=cnts[0] if len(cnts)==2 else cnts[1]

# min ve max alan degerlerinin ayarlanmasi
min_area=100
max_area=1500
image_number=0
for c in cnts:
    area=cv2.contourArea(c)
    if area>=min_area and area<=max_area:
        x,y,h,w=cv2.boundingRect(c)
        ROI=image[y:y+h,x:x+w]
        cv2.imwrite("ROI_{}.png".format(image_number),ROI)
        cv2.rectangle(image,(x,y),(x+w,y+h),(36,255,12),2)
        image_number+=1

# olusan goruntuleri ekrana gosterme
cv2.imshow("Sharpen",sharpen)
cv2.imshow("close",close)
cv2.imshow("thresh",thresh)
cv2.imshow("image",image)
cv2.waitKey()


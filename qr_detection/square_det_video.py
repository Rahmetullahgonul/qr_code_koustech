import cv2
import numpy as np

# girelecek video
cap=cv2.VideoCapture("cicikus_kamikaze.mp4")

# videoyu boyutlandrima
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

while True:
    ret,frame=cap.read()
    if not ret:
        break

    # gerekli filtreleme islemleri
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
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
    min_area=1000
    max_area=1500
    image_number=0
    for c in cnts:
        area=cv2.contourArea(c)
        if area>=min_area and area<=max_area:
            x,y,h,w=cv2.boundingRect(c)
            ROI=frame[y:y+h,x:x+w]
            cv2.imwrite("ROI_{}.png".format(image_number),ROI)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(36,255,12),2)
            image_number+=1

    # olusan goruntuyu ekrana gosterme
    cv2.imshow("Result",frame)

    if cv2.waitKey(45) & 0xFF==ord("q"):
        break

cap.read()
cv2.destroyAllWindows()

import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np

cap=cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    _,thershold=cv2.threshold(gray,200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours,hierarchy=cv2.findContours(thershold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        sorted_areas=sorted(contours,key=cv2.contourArea,reverse=True)
        largest_area=sorted_areas[0]
    rect=cv2.minAreaRect(largest_area)
    box=cv2.boxPoints(rect)
    box=np.int_(box)

    #perspektif donusumu
    width=int(rect[1][0])
    height=int(rect[1][1])
    src_corners=np.float32(box)
    dst_corners=np.array([[0,0],[width-1,0],[width-1,height-1],[0,height-1]],np.float32)
    M = cv2.getPerspectiveTransform(src_corners, dst_corners)
    
    frame=cv2.warpPerspective(frame,M,(width,height))

    decoded_objects=pyzbar.decode(frame,[pyzbar.ZBarSymbol.QRCODE])

    for obj in decoded_objects:
        print("DATA:",obj.data)
    
    cv2.imshow("FRAME",frame)

    if cv2.waitKey(1) & 0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
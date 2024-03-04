import cv2
import numpy as np
import time


cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

detector=cv2.QRCodeDetector()

while True:
    ret,frame=cap.read()
    if not ret:
        break

    start=time.perf_counter()

    value,points,qrcode=detector.detectAndDecode(frame)

    if value!="":
        x1=points[0][0][0]
        y1=points[0][0][1]
        x2=points[0][2][0]
        y2=points[0][2][1]

        x_center=(x2-x1)/2+x1
        y_center=(y2-y1)/2+y1

        cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),3)
        cv2.circle(frame,(int(x_center),int(y_center)),1,(255,0,0),1)
        cv2.putText(frame,(str(value)),(30,120),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    end=time.perf_counter()
    total_time=end-start
    fps=1/total_time

    cv2.putText(frame,f"FPS:{fps:.2f}",(30,70),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)

    cv2.imshow("QR_Detection",frame)

    if cv2.waitKey(1) & 0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()


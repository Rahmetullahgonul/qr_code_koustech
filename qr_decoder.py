import cv2
from pyzbar.pyzbar import decode

from qr import QR

cap=cv2.VideoCapture("cicikus_kamikaze.mp4")

qr_detector = QR()

while True:
    ret,frame=cap.read()

    frame=cv2.resize(frame,(720,1080))
    
    # qr kodlarini tespit et 
    data = qr_detector.decode(frame)


    # for obj in decode_objects:
    if data:
        #qr kodun icerigini almak icin
        # data=obj.data.decode('utf-8')

        # qr kodun konumunu ve icerigini ekrana yazdir
        print(f"QR CODE DATA : {data}")
        # x,y,w,h=obj.rect
        # cv2.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),2)
        # cv2.putText(frame,data,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)

    cv2.imshow("QR Code Scanner",frame)

    if cv2.waitKey(1) & 0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

    
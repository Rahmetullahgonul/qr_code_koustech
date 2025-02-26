import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap=cv2.VideoCapture("cici.mp4")

while True:
    ret,frame=cv2.imread()
    if not ret:
        break
    for qr_code in qr_codes:
        (x,y,w,h)=qr_code.rect
        cv2.rectangle((frame,(x,y),(x+w,y+h),(0,255,0),2))

        qr_code_data=qr_code.data.decodet
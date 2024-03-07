"""
NOT1 :
*qr kodu decode etmek ve tespit etmek amaciyla pyzbar kutuphanesi eklendi
*goruntu siyah beyaza donusturulup ardindan threshold islemi uygulanip
sonrasinde goruntudeki qr kodlari tespit etmeye calisildi
*ancak renkli qr kodu okumakta sorun yasiyo
*siyah beyaz qr kodlari rahat bi sekilde decode ederken yanlis yerlere detect atiyo
"""
"""
NOT2 :
*son kodun ustune bir de blurlama islemi uygulandiktan sonra elde edilen sonuclar 
daha iyi sonuclar elde ediyo ve renkli qr koda da detect ve decode atabiliyo
*daha uzak mesafelerdeki qr kodlari tespit edebiliyo 
*cicikusun videosundaki qr kodu rahat bir sekilde okuyabiliyor
"""


import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time

def detect_qr_code(frame):
    """
    QR kodlari tespit et
    """
    # videodaki gurultuyu azaltmak icin blurlama islemi
    blurred_frame=cv2.GaussianBlur(frame,(5,5),0)
    
    # siyah beyaza donusturme
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # threshold islemi
    _,thresholded=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

    # QR kodlari tespi etme
    decode_objects=decode(thresholded)


    # her bir qr kodu donguyle isleme
    for obj in decode_objects:
        # qr kodun verisini ve konumunu alma
        rect=obj.rect
        # perspektif donusturme islemi
        points = np.array([rect[:2],[rect[0],rect[1]+rect[3]],[rect[0]+rect[2],rect[1]+rect[3]],[rect[0]+rect[2],rect[1]]],dtype=np.float32)
        width=max(rect[2],rect[3])
        height=min(rect[2],rect[3])

        # hedef noktalari belirleme
        dst_points=np.array([[0,0],[0,height],[width,height],[width,0]],dtype=np.float32)

        # perspektif donusum matrislerini hesaplama
        matrix=cv2.getPerspectiveTransform(points,dst_points)

        # perspektif donusumu uygulama
        warped_frame=cv2.warpPerspective(frame,matrix,(width,height))

        # QR kodlarini tespit et
        decode_objects_warped=decode(warped_frame)

        # her bir QR kodunu isleme
        for obj_warped in decode_objects_warped:
            # QR kodun verisini ve konumunu alma
            data=obj_warped.data.decode('utf-8')

            # konumu ve veriyi ekrana yazdirma
            print("QR kodun verisi:",data)
            print("QR kodun konumu:",obj_warped.rect)

            # qr kod icin dikdortgen ciz
            cv2.rectangle(frame,(rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]),(0,255,0),2)
    return frame

def main():
    """
    QR kod tespit edilecek ana kod
    """

    # girilecek dosyanin pathini buraya ekle
    cap=cv2.VideoCapture(0)

    while True:
        ret,frame=cap.read()
        if not ret:
            print("Goruntuye ulasilamiyor!")
            break
        start = time.perf_counter()

        # QR kodlari algila
        frame_with_qr=detect_qr_code(frame)

        # ekrana fps verme
        end = time.perf_counter()
        totaltime=end-start
        fps=1/totaltime
        cv2.putText(frame, f"FPS:{fps:.2f}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # islenmis cerceveyi goster
        cv2.imshow("QR kod algilandi",frame_with_qr)

        if cv2.waitKey(1) & 0xFF==ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()

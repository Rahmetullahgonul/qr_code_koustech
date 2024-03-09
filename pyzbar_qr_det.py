#https://github.com/koustech/QR_kamikaze.git
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

"""
NOT3:
*thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
isleminden sonra dronla çekilmiş QR kodunu da okuyabilir hale geldi
*videodaki QR kodu kac kez tespit ettigini terminala yazdiriyorum
"""

"""
NOT4:
*blurred_frame=cv2.GaussianBlur(frame,(1,1),0) 
=> drone 89 kez
=> cici 214 kez
=> sufai 0 kez
=> iku 0 kez

**blurred_frame=cv2.GaussianBlur(frame,(5,5),0) 
=> drone 89 kez
=> cici 214 kez
=> sufai 0 kez
=> iku 0 kez

"""

"""
yarin bu hatalarin nedenine de bak! 
WARNING: decoder/databar.c:1248: _zbar_decode_databar: Assertion "seg->finder >= 0" failed.
	i=17 f=-1(001) part=1
WARNING: decoder/databar.c:1248: _zbar_decode_databar: Assertion "seg->finder >= 0" failed.
	i=9 f=-1(001) part=1
WARNING: decoder/databar.c:1248: _zbar_decode_databar: Assertion "seg->finder >= 0" failed.
	i=22 f=-1(001) part=1
WARNING: decoder/databar.c:1248: _zbar_decode_databar: Assertion "seg->finder >= 0" failed.
	i=23 f=-1(001) part=1
WARNING: decoder/databar.c:1248: _zbar_decode_databar: Assertion "seg->finder >= 0" failed.
	i=30 f=-1(001) part=1
"""

import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time

# define counter
counter=0
# define video path
#video pathini buraya gir
video_path= "cicikus_kamikaze.mp4"

def detect_qr_code(frame):
    """
    QR kodlari tespit et
    """

    global counter

    # videodaki gurultuyu azaltmak icin blurlama islemi
    blurred_frame=cv2.GaussianBlur(frame,(5,5),0)

    # siyah beyaza donusturme
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # threshold islemi
    thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

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
            cv2.putText(frame,(str(data)),(30,120),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            print("QR kodun konumu:",obj_warped.rect)

            # sayac
            if data!=0:
                counter=counter+1
                print(f"Videoda {counter} kez QR kod algilandi ")

            # qr kod icin dikdortgen ciz
            cv2.rectangle(frame,(rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]),(0,255,0),2)
    return frame

def main():
    """
    QR kod tespit edilecek ana kod
    """

    global video_path

    # girilecek dosyanin pathini buraya ekle
    cap=cv2.VideoCapture(video_path)

    paused=False

    while True:
        if not paused:
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
        """
        space tusu => videoyu durdur/oynat
        q tusu => videodan cik
        """
        cv2.imshow("QR kod algilandi",frame_with_qr)
        key=cv2.waitKey(1)
        if key==ord(' '):
            paused=not paused

        if key==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()
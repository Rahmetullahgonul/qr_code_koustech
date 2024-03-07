"""
qr kodu decode etmek ve tespit etmek amaciyla pyzbar kutuphanesi eklendi
goruntu siyah beyaza donusturulup ardindan threshold islemi uygulanip
sonrasinde goruntudeki qr kodlari tespit etmeye calisildi
ancak renkli qr kodu okumakta sorun yasiyo
siyah beyaz qr kodlari rahat bi sekilde decode ederken yanlis yerlere detect atiyo
"""
import cv2
from pyzbar.pyzbar import decode

def detect_qr_code(frame):
    """
    QR kodlari tespit et
    """
    
    # siyah beyaza donusturme
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # threshold islemi
    _,thresholded=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

    # QR kodlari tespi etme
    decode_objects=decode(thresholded)


    # her bir qr kodu donguyle isleme
    for obj in decode_objects:
        # qr kodun verisini ve konumunu alma
        data=obj.data.decode('utf-8')
        rect_points=obj.rect

        # konumu ve veriyi ekrana yazdirma
        print("QR kodun verisi:",data)
        print("QR kodun konumu:",rect_points)

        # qr kod icin dikdortgen ciz
        cv2.rectangle(frame,(rect_points[0],rect_points[1]),(rect_points[2],rect_points[3]),(0,255,0),2)

    return frame

def main():
    """
    QR kod tespit edilecek ana kod
    """

    cap=cv2.VideoCapture(0)

    while True:
        ret,frame=cap.read()
        if not ret:
            print("Goruntuye ulasilamiyor!")
            break

        # QR kodlari algila
        frame_with_qr=detect_qr_code(frame)

        # islenmis cerceveyi goster
        cv2.imshow("QR kod algilandi",frame_with_qr)

        if cv2.waitKey(1) & 0xFF==ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()

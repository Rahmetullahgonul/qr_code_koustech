import cv2
from pyzbar.pyzbar import decode

def detect_qr_code(frame):
    """
    QR kodlari tespit et
    """
    # goruntuyu  siyah-beyaza cevirme
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # threshhold islemi
    _,thresholded=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

    decode_objcets = decode(frame)

    # her bir qr kodu donguyle isleme
    for obj in decode_objcets:
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

    cap=cv2.VideoCapture()

    while True:
        ret,frame=cap.read()
        if not ret:
            print("Goruntu girmen lazim")
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

import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time

# define counter
counter=0
# define video path
#video pathini buraya gir
video_path= "iku_kamikaze.mp4"


def two_dimensional_otsu_threshold(frame):
    # goruntunun yukseklik ve genislik degeri
    height,width=frame.shape

    # videodaki gurultuyu azaltmak icin blurlama islemi
    frame=cv2.GaussianBlur(frame,(5,5),0)

    # siyah beyaza donusturme
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


    # goruntunun histogramini hesapla
    hist=cv2.calcHist([frame],[0],None,[256],[0,256])

    # tum piksel sayisini hesaplama
    total_pixels=height*width

    # olasilik ve kumulatif olasilik matrislerini baslat
    probability=hist/total_pixels
    cumulative_probability=np.cumsum(probability)

    # tum olasi degerleri deneyerek arka plan ve on plan arasindaki
    # varyans degerini hesaplama
    max_variance=0
    optimal_threshold=0

    for t in range(256):
        # arka plan ve on plan piksel olasiliklarini hesaplama
        prob_background=cumulative_probability[t]
        prob_foreground=1-prob_background

        # arka plan ve on plan ortalamalarini hesapla
        mean_background=np.sum(np.arange(t)*probability[:t])/prob_background
        mean_foreground=np.sum(np.arange(t,256)*probability[t:])/prob_foreground

        # arka plan ve on plan varyanslari hesabi
        variance_background=np.sum(((np.arange(t)-mean_background)**2)*probability[:t])/prob_background
        variance_foreground=np.sum(((np.arange(t,256)-mean_foreground)** 2)*probability[t:])/prob_foreground

        # toplam varyans hesabi
        total_variance=prob_background*variance_background+prob_foreground*variance_foreground

        # max varyans ve optimum esik degerini guncelle
        if total_variance>max_variance:
            max_variance=total_variance
            optimal_threshold=t


    # optiumum esik degerine gore kullanarak goruntuyu isle
    _,processed_frame=cv2.threshold(frame,optimal_threshold,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    frame=processed_frame
    return frame

def detect_qr_code(frame):
    """
    QR kodlari tespit et
    """

    global counter
    """
    # gurultu azaltmak icin blur atma islemi
    blurred_frame=cv2.GaussianBlur(frame,(5,5),0)

    #siyah beyaza donusturme
    gray_frame=cv2.cvtColor(blurred_frame,cv2.COLOR_BGR2GRAY)
    """
    # QR kodlari tespi etme
    decode_objects=decode(frame)


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
        cv2.putText(frame, f"FPS:{fps:.0f}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

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
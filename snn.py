import cv2
import numpy as np
import time

class SpikingNeuralNetwork:
    def __init__(self, input_shape):
        self.input_shape = input_shape
        self.weights = np.random.rand(*input_shape)  # Giriş boyutuna uygun olarak ağırlıkları oluştur
        self.thresholds = np.random.rand(input_shape[0])  # Eşiklerin boyutunu giriş boyutu ile aynı yap
        self.membrane_potentials = np.zeros(input_shape[0])

    def process_frame(self, frame):
        # Kare boyutunu ayarla
        frame_resized = cv2.resize(frame, (self.input_shape[1],self.input_shape[0]))

        # Aktivasyonları hesapla
        activations = np.sum(np.multiply(frame_resized, self.weights), axis=-1)

        # Her bir piksel için eşik değeri hesapla
        threshold_matrix = np.tile(self.thresholds, (self.input_shape[1], 1)).T

        # Hucreleri atesleme ve eşiklerini kontrol etme
        firing_mask = activations >= threshold_matrix
        self.membrane_potentials[firing_mask] = 0
        self.membrane_potentials[~firing_mask] += activations[~firing_mask]

        return frame_resized

def main():
    cap = cv2.VideoCapture(0)
    paused = False
    snn = SpikingNeuralNetwork(input_shape=(480, 640, 3))  # Giriş boyutunu uygun şekilde ayarla

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("Görüntü alınamıyor!")
                break

        start = time.perf_counter()

        # Kareyi işle
        frame_with_qr = snn.process_frame(frame)

        # Ekrana FPS ekle
        end = time.perf_counter()
        total_time = end - start
        fps = 1 / total_time
        cv2.putText(frame_with_qr, f"FPS: {fps:.2f}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # İşlenmiş kareyi göster
        cv2.imshow("QR kod algılandı", frame_with_qr)
        key = cv2.waitKey(1)

        if key == ord(' '):
            paused = not paused

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

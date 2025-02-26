import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
from pyzbar_qr_det import detect_qr_code

class QRCodeReader:
    def __init__(self, video_source):
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.root = Tk()
        self.root.title("QR Kod Okuyucu")
        self.playing = True
        self.speed = 10.0

        self.video_frame = Frame(self.root)
        self.video_frame.pack()

        self.canvas = Canvas(self.video_frame)
        self.canvas.pack()

        self.control_frame = Frame(self.root)
        self.control_frame.pack()

        self.play_button = Button(self.control_frame, text="Oynat/Durdur", command=self.toggle_play)
        self.play_button.grid(row=0, column=0)

        self.speed_label = Label(self.control_frame, text="Oynatma Hızı: ")
        self.speed_label.grid(row=0, column=1)
        self.speed_scale = Scale(self.control_frame, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL, command=self.change_speed)
        self.speed_scale.set(self.speed)
        self.speed_scale.grid(row=0, column=2)

        self.change_video_button = Button(self.control_frame, text="Video Değiştir", command=self.change_video)
        self.change_video_button.grid(row=0, column=3)

        self.update()

        self.root.mainloop()

    def toggle_play(self):
        self.playing = not self.playing

    def change_speed(self, speed):
        self.speed = float(speed)

    def change_video(self):
        new_video_source = filedialog.askopenfilename()
        if new_video_source:
            self.video_source = new_video_source
            self.cap = cv2.VideoCapture(new_video_source)

    def update(self):
        if self.playing:
            ret, frame = self.cap.read()
            if ret:
                frame = self.detect_qr_code(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.imgtk = imgtk
                self.canvas.create_image(0, 0, anchor=NW, image=imgtk)
            else:
                self.playing = False

        self.root.after(int(1000 / self.speed), self.update)

    def detect_qr_code(self, frame):
        # Kodu burada tespit etme işlemlerini yapabilirsiniz
        detect_qr_code(frame)
        return frame

if __name__ == "__main__":
    QRCodeReader(0)

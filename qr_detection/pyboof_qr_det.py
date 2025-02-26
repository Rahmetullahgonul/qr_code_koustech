import numpy as np
import pyboof as pb

data_path = "cicikus_kamikaze.mp4"

# Load video as GrayU8 (single band, 8-bit grayscale) image
video = pb.load_single_band(data_path, np.uint8)

# Create QR code detector
detector = pb.FactoryFiducial(np.uint8).qrcode()

# Process each frame in the video
while video.next_frame():
    # Detect QR codes in the current frame
    detector.detect(video)

    # Print the number of detected QR codes in the frame
    print("Detected a total of {} QR codes".format(len(detector.detections)))

    # Print message and bounds of each detected QR code
    for qr in detector.detections:
        print("Message: " + qr.message)
        print("Bounds: " + str(qr.bounds))

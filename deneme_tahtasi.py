import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time

# define counter
counter = 0
# define video path
video_path = "iku_kamikaze.mp4"

def preprocess(frame):
    """
    Apply preprocessing steps to improve QR code detection.
    """
    global counter

    # Blur the frame to reduce noise
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # Convert to grayscale
    gray = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

    # Adaptive thresholding
    thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Find contours and filter using a minimum size
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = 50
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    # Draw rectangles around the QR codes
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Crop the QR code
        qr_code = gray[y:y + h, x:x + w]

        # Perspective transformation
        src_points = np.array([[0, 0], [0, h], [w, h], [w, 0]], dtype=np.float32)
        dst_points = np.array([[0, 0], [0, h], [h, w], [0, w]], dtype=np.float32)
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        warped_qr_code = cv2.warpPerspective(qr_code, matrix, (h, w))

        # Decode the QR code
        decode_objects = decode(warped_qr_code)

        # Process each decoded QR code
        for obj in decode_objects:
            data = obj.data.decode("utf-8")

            # Display the data and position
            print("QR code data:", data)
            cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            print("QR code position:", (x, y))

            # Increment the counter
            if data != "0":
                counter += 1
                print(f"QR code detected {counter} times in the video")

    return frame

def main():
    """
    QR code detection in the video.
    """

    global video_path

    cap = cv2.VideoCapture(video_path)

    paused = False

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("Cannot access the video!")
                break

        start = time.perf_counter()

        # Preprocess and detect QR codes
        frame_with_qr = preprocess(frame)

        # Display FPS
        end = time.perf_counter()
        totaltime = end - start
        fps = 1 / totaltime
        cv2.putText(frame, f"FPS:{fps:.0f}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("QR code detection", frame_with_qr)
        
        key=cv2.waitKey(15)
        if key==ord(' '):
            paused=not paused

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()
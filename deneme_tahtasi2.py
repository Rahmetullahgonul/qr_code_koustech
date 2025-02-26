import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import time

# define counter
counter = 0
# define video path
video_path = "qr_sufai.mp4"
paused=False


def detect_qr_code(frame):
    """
    Detect QR codes
    """
    global counter

    # blur frame to reduce noise
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # apply adaptive thresholding
    thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # find contours
    contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find the largest contour
    for cnt in contours:
        area = cv2.contourArea(cnt)
        sorted_areas = sorted(contours, key=cv2.contourArea, reverse=True)
        largest_area = sorted_areas[0]

    rect = cv2.minAreaRect(largest_area)
    box = cv2.boxPoints(rect)
    box = np.int_(box)

    # apply perspective transform
    width = int(rect[1][0])
    height = int(rect[1][1])
    src_corners = np.float32(box)
    dst_corners = np.array([[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]], np.float32)
    M = cv2.getPerspectiveTransform(src_corners, dst_corners)
    frame = cv2.warpPerspective(frame, M, (width, height))

    # decode QR codes
    decode_objects = pyzbar.decode(thresholded, [pyzbar.ZBarSymbol.QRCODE])

    # process each QR code
    for obj in decode_objects:
        # get data and location
        data = obj.data.decode('utf-8')

        # print data and location
        print("QR code data: {}, location: {}".format(data, obj.rect))

        # increment counter
        if data:
            counter += 1
            print("QR code detected {} times in the video".format(counter))

        # draw rectangle around QR code
        cv2.rectangle(frame, (obj.rect[0], obj.rect[1]), (obj.rect[0]+obj.rect[2], obj.rect[1]+obj.rect[3]), (0, 255, 0), 2)

    return frame

def main():
    """
    Main function to detect QR codes
    """



        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    print("Cannot read video!")
                    break
            
            start=time.perf_counter()

            # detect QR codes
            frame_with_qr = detect_qr_code(frame)

            # display FPS
            end = time.perf_counter()
            totaltime = end-start
            fps = 1 / totaltime
            cv2.putText(frame, f"FPS: {fps:.0f}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # display frame
            cv2.imshow("QR code detected", frame_with_qr)
            key = cv2.waitKey(15)

            if key == ord(' '):
                paused = not paused

            if key == ord('q'):
                break

if __name__ == "__main__":
    main()
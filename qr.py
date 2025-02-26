import cv2


class QR:
    def __init__(self):
        pass

    def points_setting(self,points):
        x1, y1 = list(points)[0][0][0], list(points)[0][0][1]
        x2, y2 = list(points)[0][1][0], list(points)[0][1][1]
        x3, y3 = list(points)[0][2][0], list(points)[0][2][1]
        x4, y4 = list(points)[0][3][0], list(points)[0][3][1]
        p1 = (int(x1),int(y1))
        p2 = (int(x2),int(y2))
        p3 = (int(x3),int(y3))
        p4 = (int(x4),int(y4))
        return p1,p2,p3,p4

    def image_points_line(self,points,image):
        # print(points)

        en_kucuk_x = points[3][0]
        en_buyuk_x = points[2][0]

        en_kucuk_y = points[0][1]
        en_buyuk_y = points[3][1]

        cv2.line(image, points[0], points[1], color=(0,255,0), thickness=9)
        cv2.line(image, points[1], points[2], color=(0, 255, 0), thickness=9)
        cv2.line(image, points[2], points[3], color=(0, 255, 0), thickness=9)
        cv2.line(image, points[3], points[0], color=(0, 255, 0), thickness=9)

        copy_img = image
        # print(copy_img.shape)
        cropped_image = copy_img[en_kucuk_y:en_kucuk_y+(en_buyuk_y-en_kucuk_y), en_kucuk_x:en_kucuk_x+(en_buyuk_x-en_kucuk_x)]
        # print(cropped_image.shape)
        cv2.imshow("normal",image)
        cv2.imshow("crop.jpg", cropped_image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def decode(self,image):
        qrCodeDetector = cv2.QRCodeDetector()
        decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
        # print(result)
        if points is not None:
            self.image_points_line(self.points_setting(points),image)
            print(decodedText)
            return decodedText
        else:
            return False

import cv2


detector = cv2.QRCodeDetector()

img = cv2.imread('images/1.jpg')

qr_data = detector.detectAndDecode(img)[0]


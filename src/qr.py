import cv2


def detect_qr_code(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return None

    qr_detector = cv2.QRCodeDetector()
    qr_text, points, _ = qr_detector.detectAndDecode(image)

    if qr_text:
        return qr_text

    return None
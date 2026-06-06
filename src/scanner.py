import cv2
import numpy as np


def resize_image(image, height=800):
    ratio = height / image.shape[0]
    width = int(image.shape[1] * ratio)

    resized_image = cv2.resize(image, (width, height))

    return resized_image, ratio


def find_document_contour(edge_image):
    contours, _ = cv2.findContours(
        edge_image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        corners = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(corners) == 4:
            return corners

    return None


def order_points(points):
    points = points.reshape(4, 2)

    ordered_points = np.zeros((4, 2), dtype="float32")

    total = points.sum(axis=1)
    difference = np.diff(points, axis=1)

    ordered_points[0] = points[np.argmin(total)]
    ordered_points[1] = points[np.argmin(difference)]
    ordered_points[2] = points[np.argmax(total)]
    ordered_points[3] = points[np.argmax(difference)]

    return ordered_points


def transform_perspective(image, points):
    ordered_points = order_points(points)

    top_left, top_right, bottom_right, bottom_left = ordered_points

    width_bottom = np.linalg.norm(bottom_right - bottom_left)
    width_top = np.linalg.norm(top_right - top_left)
    final_width = int(max(width_bottom, width_top))

    height_right = np.linalg.norm(top_right - bottom_right)
    height_left = np.linalg.norm(top_left - bottom_left)
    final_height = int(max(height_right, height_left))

    destination_points = np.array(
        [
            [0, 0],
            [final_width - 1, 0],
            [final_width - 1, final_height - 1],
            [0, final_height - 1],
        ],
        dtype="float32"
    )

    matrix = cv2.getPerspectiveTransform(ordered_points, destination_points)
    scanned_image = cv2.warpPerspective(image, matrix, (final_width, final_height))

    return scanned_image


def enhance_scan(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    enhanced_image = cv2.adaptiveThreshold(
        gray_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return enhanced_image


def scan_document(input_path, output_path):
    original_image = cv2.imread(input_path)

    if original_image is None:
        raise ValueError("Image not found. Please check the input path.")

    resized_image, ratio = resize_image(original_image)

    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edge_image = cv2.Canny(blurred_image, 75, 200)

    document_contour = find_document_contour(edge_image)

    if document_contour is None:
        raise ValueError("Could not detect document edges.")

    document_contour = document_contour.reshape(4, 2) / ratio

    scanned_image = transform_perspective(original_image, document_contour)
    enhanced_image = enhance_scan(scanned_image)

    cv2.imwrite(output_path, enhanced_image)

    return output_path
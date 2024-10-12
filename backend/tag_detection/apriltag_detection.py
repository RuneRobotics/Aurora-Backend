import cv2
import numpy as np
import pyapriltags as apriltag
import json
import os

def get_camera_matrix():
    return np.array([[600, 0, 320],  # fx, 0, cx
                          [0, 600, 240],  # 0, fy, cy
                          [0, 0, 1]], dtype=np.float32)

def get_camera_dist_coeffs():
    return np.zeros((4, 1))


def load_json(path: str):
    with open(path, 'r') as file:
        data = json.load(file)
    return data


json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'apriltag_data', 'apriltags_layout.json')
field_data = load_json(json_file_path)

camera_matrix = get_camera_matrix()
dist_coeffs = get_camera_dist_coeffs()

detector = apriltag.Detector(families='tag36h11')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags in the image
    detections = detector.detect(gray)

    world_points = []
    image_points = []

    for detection in detections:
        tag_id = detection.tag_id
        image_corners = np.array(detection.corners, dtype=np.float32)

        # Draw green square around detected AprilTags
        corners_int = np.array(detection.corners, dtype=np.int32)
        cv2.polylines(frame, [corners_int.reshape((-1, 1, 2))], isClosed=True, color=(0, 255, 0), thickness=2)

        # Display the frame
    cv2.imshow("Detected AprilTags", frame)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
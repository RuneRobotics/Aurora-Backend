import cv2
import numpy as np
import json
from camera import Camera

def load_json(path: str):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def calculate_position():
    pass

def detect_ats(frame, detector, field_data, camera: Camera):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray_frame)

    camera_matrix = camera.matrix
    dist_coeffs = camera.dist_coeffs

    world_points = []
    image_points = []

    for detection in detections:
        tag_id = detection.tag_id
        image_corners = np.array(detection.corners, dtype=np.float32)

        # Draw green square around detected AprilTags
        corners_int = np.array(detection.corners, dtype=np.int32)
        cv2.polylines(frame, [corners_int.reshape((-1, 1, 2))], isClosed=True, color=(0, 255, 0), thickness=2)

    return {}

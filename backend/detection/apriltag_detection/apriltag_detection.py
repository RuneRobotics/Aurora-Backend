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

def detect_ats(frame, detector):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray_frame)

    world_points = []
    image_points = []

    for detection in detections:
        tag_id = detection.tag_id
        image_corners = np.array(detection.corners, dtype=np.float32)

        # Draw green square around detected AprilTags
        corners_int = np.array(detection.corners, dtype=np.int32)
        cv2.polylines(frame, [corners_int.reshape((-1, 1, 2))], isClosed=True, color=(0, 255, 0), thickness=2)

    return detections

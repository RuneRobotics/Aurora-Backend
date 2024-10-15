import cv2
import numpy as np
import json
import os
from camera import Camera, position_relative_to_camera
import math

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

    detected_atags = []

    for detection in detections:
        tag_id = detection.tag_id

        tags_data = {}

        with open(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'apriltag_data', 'apriltags_layout.json'), 'r') as file:
            tags_data = json.load(file)

        tag_pose = tags_data["tags"][tag_id - 1]["pose"]
        tag_x = tag_pose["translation"]["x"]
        tag_y = tag_pose["translation"]["y"]
        tag_z = tag_pose["translation"]["z"]

        tag_theta = 2 * math.acos(tag_pose["rotation"]["quaternion"]["W"])

        image_corners = np.array(detection.corners, dtype=np.float32)
        atag_half_size = 0.5 * ((6.5 * 2.54) / 100) # inch to cm to m

        world_corners = np.array([
                                [tag_x + atag_half_size * np.cos(tag_theta - np.pi), tag_y + atag_half_size * np.sin(tag_theta - np.pi), tag_z + atag_half_size],  # Top-left corner
                                [tag_x - atag_half_size * np.cos(tag_theta - np.pi), tag_y - atag_half_size * np.sin(tag_theta - np.pi), tag_z + atag_half_size],   # Top-right corner
                                [tag_x - atag_half_size * np.cos(tag_theta - np.pi), tag_y - atag_half_size * np.sin(tag_theta - np.pi), tag_z - atag_half_size],    # Bottom-right corner
                                [tag_x + atag_half_size * np.cos(tag_theta - np.pi), tag_y + atag_half_size * np.sin(tag_theta - np.pi), tag_z - atag_half_size]    # Bottom-left corner
                                ], dtype=np.float32)

        if image_corners.shape[0] == 4:
            _, rvec, tvec = cv2.solvePnP(world_corners, image_corners, camera_matrix, dist_coeffs)
        else:
            print(f"Tag {tag_id} did not return exactly 4 corners.")

        rotation_matrix, _ = cv2.Rodrigues(rvec)
        camera_position = -np.dot(rotation_matrix.T, tvec)
        x_world, y_world, z_world = camera_position.flatten()
        pitch, yaw, roll = cv2.decomposeProjectionMatrix(np.hstack((rotation_matrix, tvec)))[6]

        corners_int = np.array(detection.corners, dtype=np.int32)
        cv2.polylines(frame, [corners_int.reshape((-1, 1, 2))], isClosed=True, color=(180, 30, 120), thickness=2)

        detected_atags.append({"id": tag_id, "camera position": {"x": x_world, "y": y_world, "z": z_world, "roll": roll[0], "pitch": pitch[0], "yaw": yaw[0]}, "distances from camera": {"x": abs(x_world - tag_x), "y": abs(y_world - tag_y), "z": abs(z_world - tag_z)}, "score": 1})

        print("total dist:", np.sqrt((x_world - tag_x)**2 + (x_world - tag_x)**2 + (x_world - tag_x)**2))

    return {"april tags": detected_atags} | {"robot location": {"x": 0, "y": 0, "z": 0}}

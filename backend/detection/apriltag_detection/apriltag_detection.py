import cv2
import numpy as np
import json
import os
from camera import Camera, position_relative_to_camera
import math
import pyapriltags as apriltag

def get_camera_pose(tag_world_corners, tag_image_corners, camera_matrix, dist_coeffs):
    success, rvec, tvec = cv2.solvePnP(tag_world_corners, tag_image_corners, camera_matrix, dist_coeffs)

    if not success:
        raise Exception("SolvePnP failed to find a solution.")
    
    rotation_matrix, _ = cv2.Rodrigues(rvec)
    
    rotation_matrix_inv = rotation_matrix.T
    
    camera_position = -rotation_matrix_inv @ tvec
    
    def rotation_matrix_to_euler_angles(R):
        sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
        singular = sy < 1e-6

        if not singular:
            roll = np.arctan2(R[2, 1], R[2, 2])
            pitch = np.arctan2(-R[2, 0], sy)
            yaw = np.arctan2(R[1, 0], R[0, 0])
        else:
            roll = np.arctan2(-R[1, 2], R[1, 1])
            pitch = np.arctan2(-R[2, 0], sy)
            yaw = 0

        return np.array([roll, pitch, yaw])

    euler_angles = rotation_matrix_to_euler_angles(rotation_matrix_inv)
    
    camera_position = camera_position.flatten()
    euler_angles = np.degrees(euler_angles)

    return camera_position, euler_angles

def compute_tag_world_corners(tag_x_world, tag_y_world, tag_z_world, tag_theta_world, tag_half_size):

    cos = np.cos(np.pi - tag_theta_world)
    sin = np.sin(np.pi - tag_theta_world)

    local_corners = np.array([
        [tag_half_size, tag_half_size, -tag_half_size],   # Bottom left
        [-tag_half_size, -tag_half_size, -tag_half_size],   # Bottom right
        [-tag_half_size, -tag_half_size, tag_half_size],    # Top right
        [tag_half_size, tag_half_size, tag_half_size]   # Top left
    ])
    
    tag_world_corners = []
    for corner in local_corners:
        x_local, y_local, z_local = corner
        
        x_rotated = x_local * sin
        y_rotated = x_local * cos

        x_world = tag_x_world + x_rotated
        y_world = tag_y_world + y_rotated
        z_world = tag_z_world + z_local

        tag_world_corners.append([x_world, y_world, z_world])

    return np.array(tag_world_corners, dtype=np.float32)

def detect_ats(frame, detector, field_data, camera: Camera):

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray_frame)

    camera_matrix = camera.matrix
    dist_coeffs = camera.dist_coeffs
    
    tag_half_size = 0.5 * ((6.5 * 2.54) / 100)  # Convert from inches to meters

    detected_atags = []

    for detection in detections:
        tag_id = detection.tag_id
        tag_pose = field_data["tags"][tag_id - 1]["pose"]
        tag_x_world = tag_pose["translation"]["x"]
        tag_y_world = tag_pose["translation"]["y"]
        tag_z_world = tag_pose["translation"]["z"]
        tag_theta_world = 2 * math.acos(tag_pose["rotation"]["quaternion"]["W"])

        tag_image_corners = np.array(detection.corners, dtype=np.float32)

        tag_world_corners = compute_tag_world_corners(tag_x_world, tag_y_world, tag_z_world, tag_theta_world, tag_half_size)

        print(tag_world_corners)
        print(tag_image_corners)
        print("##################################")

        camera_position, euler_angles = get_camera_pose(tag_world_corners, tag_image_corners, camera_matrix, dist_coeffs)

        camera_x_world, camera_y_world, camera_z_world = camera_position
        camera_roll_world, camera_pitch_world, camera_yaw_world = euler_angles

        corners_int = np.array(detection.corners, dtype=np.int32)
        cv2.polylines(frame, [corners_int.reshape((-1, 1, 2))], isClosed=True, color=(255, 110, 200), thickness=6)

        detected_atags.append({
            "id": tag_id, 
            "camera_position": {"x": camera_x_world, 
                                "y": camera_y_world, 
                                "z": camera_z_world, 
                                "roll": camera_roll_world, 
                                "pitch": camera_pitch_world, 
                                "yaw": camera_yaw_world},
            "distances_from_camera": {"x": (dist_x := abs(camera_x_world - tag_x_world)), 
                                      "y": (dist_y := abs(camera_y_world - tag_y_world)), 
                                      "z": (dist_z := abs(camera_z_world - tag_z_world))},
            "score": detection.decision_margin / 100,
            "total_distance": np.sqrt(dist_x**2 + dist_y**2 + dist_z**2)
        })

    return {"april_tags": detected_atags, "robot_location": {"x": 0, "y": 0, "z": 0}}

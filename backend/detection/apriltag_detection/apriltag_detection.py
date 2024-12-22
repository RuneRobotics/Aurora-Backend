import cv2
import numpy as np
import json
import os
from camera import Camera
import math
import pyapriltags as apriltag
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    tag_euler_angles = rotation_matrix_to_euler_angles(rotation_matrix)
    
    camera_position = camera_position.flatten()
    euler_angles = np.degrees(euler_angles)
    tag_euler_angles = np.degrees(tag_euler_angles)

    return camera_position, euler_angles, tvec.flatten(), tag_euler_angles


def calculate_tag_world_corners(tag_pose):

    # MOVE TO A DIFFERENT FILE AND DO THAT ELSEWHERE
    tag_half_size = 0.5 * ((6.5 * 2.54) / 100)  # Convert from inches to meters

    tag_x_world = tag_pose["translation"]["x"]
    tag_y_world = tag_pose["translation"]["y"]
    tag_z_world = tag_pose["translation"]["z"]
    tag_theta_world = 2 * math.acos(tag_pose["rotation"]["quaternion"]["W"])

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


def calculate_tag_data(tag_position, tag_euler_angles, tag_id, tag_score):

    position = {"x": tag_position[0],
                "y": tag_position[1],
                "z": tag_position[2],
                "roll": tag_euler_angles[0],
                "pitch": tag_euler_angles[1],
                "yaw": tag_euler_angles[2]}

    return {"position": position, "certainty": tag_score, "id": tag_id}


def calculate_camera_position(camera_positions):

    total_scores = sum(position[2] for position in camera_positions)
    
    if total_scores == 0:
        return {}

    weighted_camera_position = [0, 0, 0]
    weighted_euler_angles = [0, 0, 0]
    
    for position in camera_positions:
        camera_position, euler_angles, score = position
        weight = score / total_scores
        
        camera_x_world, camera_y_world, camera_z_world = camera_position
        camera_roll_world, camera_pitch_world, camera_yaw_world = euler_angles

        weighted_camera_position[0] += camera_x_world * weight
        weighted_camera_position[1] += camera_y_world * weight
        weighted_camera_position[2] += camera_z_world * weight
        
        weighted_euler_angles[0] += camera_roll_world * weight
        weighted_euler_angles[1] += camera_pitch_world * weight
        weighted_euler_angles[2] += camera_yaw_world * weight

    return {
            "x": weighted_camera_position[0],
            "y": weighted_camera_position[1],
            "z": weighted_camera_position[2],
            "roll": weighted_euler_angles[0],
            "pitch": weighted_euler_angles[1],
            "yaw": weighted_euler_angles[2]
            }


def detect_apriltags(detector, field_data, camera: Camera, frame):

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    camera_matrix = camera.matrix
    dist_coeffs = camera.dist_coeffs
    detected_apriltags = []
    camera_positions = []
    pose = {}

    detections = detector.detect(gray_frame)

    if len(detections) == 0:
        return {}, {}

    for detection in detections:

        tag_id = detection.tag_id

        try:
            tag_pose = field_data["tags"][tag_id - 1]["pose"]
        except IndexError:
            logging.error(f"Error: tag_id {tag_id} is out of bounds.")
            continue

        tag_image_corners = np.array(detection.corners, dtype=np.float32)
        tag_world_corners = calculate_tag_world_corners(tag_pose)

        try:
            camera_position, euler_angles, tag_position, tag_euler_angles = get_camera_pose(tag_world_corners, 
                                                                                            tag_image_corners, 
                                                                                            camera_matrix, 
                                                                                            dist_coeffs)
        except Exception as e:
            logging.error(f"Error: {e}. An exception occurred while attempting to use solve PnP.")
            continue

        corners_int = np.array(detection.corners, dtype=np.int32)
        cv2.polylines(frame, [corners_int.reshape((-1, 1, 2))], isClosed=True, color=(255, 110, 200), thickness=6)

        tag_data = calculate_tag_data(tag_position, tag_euler_angles, tag_id, 1) # 1 should be replaced with the tag certainty
        detected_apriltags.append(tag_data)
        camera_positions.append((camera_position, euler_angles, 1)) # 1 should be replaced with the tag certainty

    camera_position = calculate_camera_position(camera_positions)

    return camera_position, detected_apriltags
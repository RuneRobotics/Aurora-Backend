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

def compute_tag_corners(tag_x, tag_y, tag_z, theta, half_size):
    """
    Computes the 3D world coordinates of the four corners of an AprilTag given its center, rotation, and size.
    
    Parameters:
    - tag_x, tag_y, tag_z: The 3D world coordinates of the center of the tag.
    - theta: The rotation of the tag around the Z-axis in radians.
    - half_size: Half of the size of the tag (distance from the center to any corner).
    
    Returns:
    - world_corners: The 3D coordinates of the four corners of the tag in the world frame.
    """
    
    # Calculate the cosine and sine of the rotation angle
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    # Define the four corners in the local tag coordinate system (relative to the center)
    local_corners = np.array([
        [-half_size, half_size],   # Top-left
        [half_size, half_size],    # Top-right
        [half_size, -half_size],   # Bottom-right
        [-half_size, -half_size]   # Bottom-left
    ])
    
    # Rotate the local corners by theta around the Z-axis and translate to the global (world) position
    world_corners = []
    for corner in local_corners:
        x_local, y_local = corner
        # Apply rotation
        x_rotated = x_local * cos_theta - y_local * sin_theta
        y_rotated = x_local * sin_theta + y_local * cos_theta
        # Translate to world position
        x_world = tag_x + x_rotated
        y_world = tag_y + y_rotated
        # Z remains the same since the tag is parallel to the XY-plane
        world_corners.append([x_world, y_world, tag_z])

    return np.array(world_corners, dtype=np.float32)

def get_camera_pose(world_points, image_points, camera_matrix, dist_coeffs):
    """
    This function computes the camera's position (X, Y, Z) and orientation (roll, pitch, yaw)
    in the world coordinate system.
    
    Parameters:
    - world_points: 3D world points (Nx3 array).
    - image_points: 2D image points (Nx2 array).
    - camera_matrix: Camera intrinsic matrix (3x3).
    - dist_coeffs: Distortion coefficients (1x4 or 1x5).
    
    Returns:
    - camera_position: (X, Y, Z) of the camera in the world coordinate system.
    - euler_angles: (roll, pitch, yaw) of the camera in the world coordinate system.
    """
    # Step 1: SolvePnP to get the object's rotation and translation vectors (relative to the camera)
    success, rvec, tvec = cv2.solvePnP(world_points, image_points, camera_matrix, dist_coeffs)

    if not success:
        raise Exception("SolvePnP failed to find a solution.")
    
    # Step 2: Convert the rotation vector to a rotation matrix
    rotation_matrix, _ = cv2.Rodrigues(rvec)
    
    # Step 3: Invert the rotation and translation to get the camera pose in world coordinates
    # Inverted rotation matrix (transpose of rotation_matrix)
    rotation_matrix_inv = rotation_matrix.T
    
    # Inverted translation (camera position in world coordinates)
    camera_position = -rotation_matrix_inv @ tvec
    
    # Step 4: Extract roll, pitch, and yaw (Euler angles) from the inverted rotation matrix
    # Use standard formula to convert rotation matrix to Euler angles (roll, pitch, yaw)
    def rotation_matrix_to_euler_angles(R):
        sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
        singular = sy < 1e-6  # Check for singularity

        if not singular:
            roll = np.arctan2(R[2, 1], R[2, 2])
            pitch = np.arctan2(-R[2, 0], sy)
            yaw = np.arctan2(R[1, 0], R[0, 0])
        else:
            roll = np.arctan2(-R[1, 2], R[1, 1])
            pitch = np.arctan2(-R[2, 0], sy)
            yaw = 0

        return np.array([roll, pitch, yaw])

    # Compute Euler angles (roll, pitch, yaw)
    euler_angles = rotation_matrix_to_euler_angles(rotation_matrix_inv)
    
    # Convert camera position and Euler angles to more readable format (degrees)
    camera_position = camera_position.flatten()  # (X, Y, Z)
    euler_angles = np.degrees(euler_angles)      # Convert radian to degrees (Roll, Pitch, Yaw)
    
    return camera_position, euler_angles


def detect_ats(frame, detector, field_data, camera: Camera):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray_frame)

    camera_matrix = camera.matrix
    dist_coeffs = camera.dist_coeffs

    detected_atags = []
    
    tags_data = {}

    with open(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'apriltag_data', 'apriltags_layout.json'), 'r') as file:
            tags_data = json.load(file)

    for detection in detections:
        tag_id = detection.tag_id

        tag_pose = tags_data["tags"][tag_id - 1]["pose"]
        tag_x = tag_pose["translation"]["x"]
        tag_y = tag_pose["translation"]["y"]
        tag_z = tag_pose["translation"]["z"]

        tag_theta = 2 * math.acos(tag_pose["rotation"]["quaternion"]["W"])

        image_corners = np.array(detection.corners, dtype=np.float32)
        atag_half_size = 0.5 * ((6.5 * 2.54) / 100) # inch to cm to m

        world_corners = compute_tag_corners(tag_x, tag_z, tag_y, tag_theta, atag_half_size)
        
        camera_position, euler_angles = get_camera_pose(world_corners, image_corners, camera_matrix, dist_coeffs)

        x_world, y_world, z_world = camera_position
        roll, pitch, yaw = euler_angles

        corners_int = np.array(detection.corners, dtype=np.int32)
        cv2.polylines(frame, [corners_int.reshape((-1, 1, 2))], isClosed=True, color=(180, 30, 120), thickness=6)

        detected_atags.append({"id": tag_id, "camera position": {"x": x_world, "y": y_world, "z": z_world, "roll": roll, "pitch": pitch, "yaw": yaw}, "distances from camera": {"x": abs(x_world - tag_x), "y": abs(y_world - tag_y), "z": abs(z_world - tag_z)}, "score": 1, "total distance": np.sqrt((x_world - tag_x)**2 + (x_world - tag_x)**2 + (x_world - tag_x)**2)})

    return {"april tags": detected_atags} | {"robot location": {"x": 0, "y": 0, "z": 0}}

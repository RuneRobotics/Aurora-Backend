from capture.camera import Camera, Pose3D
from utils.json_utils import load_field
from utils import constants
import pyapriltags as apriltag
from pathlib import Path
import numpy as np
import logging
import math
import cv2

class AprilTagDetector:

    def __init__(self, season: str, camera: Camera, families: str='tag36h11'):

        self.__detector = apriltag.Detector(families=families)
        self.camera = camera
        self.camera_matrix = camera.matrix
        self.dist_coeffs = camera.dist_coeffs
        self.field_data = load_field(season)


    def __detect(self, frame):
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.__detector.detect(gray_frame)
    

    def get_camera_and_tags_data(self, frame):

        detected_apriltags = []
        camera_poses = []
        
        detections = self.__detect(frame=frame)

        if len(detections) == 0:
            return constants.UNKNOWN, constants.UNKNOWN

        for tag in detections:

            tag_id = tag.tag_id

            try:
                tag_pose = self.field_data["tags"][tag_id - 1]["pose"]
            except IndexError:
                logging.error(f"Error: tag_id {tag_id} is out of bounds.")
                continue

            tag_image_corners = np.array(tag.corners, dtype=np.float32)
            tag_world_corners = self.__get_tag_world_corners(tag_pose)

            try:
                camera_position, euler_angles = self.__get_camera_pose(tag_world_corners, tag_image_corners,)
            except Exception as e:
                logging.error(f"Error: {e}. An exception occurred while attempting to use solve PnP.")
                continue

            corners_int = np.array(tag.corners, dtype=np.int32)
            frame = cv2.polylines(frame, 
                                  [corners_int.reshape((-1, 1, 2))], 
                                  isClosed=True, 
                                  color=constants.PURPLE,
                                  thickness=6)

            detected_apriltags.append(tag_id)
            camera_poses.append((camera_position, euler_angles, 1)) # 1 should be replaced with the tag certainty

        self.camera.frame = frame
        camera_position = self.__get_weighted_camera_pose(camera_poses)
        self.camera.deteceted_apriltags = detected_apriltags
        self.camera.field_pose = camera_position
        robot_pose = self.camera.get_robot_pose()
        self.camera.add_pose_to_queue(robot_pose)
    
    
    def __get_weighted_camera_pose(self, camera_positions):

        total_scores = sum(position[2] for position in camera_positions)
        
        if total_scores == 0:
            return None

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

        return Pose3D(x=weighted_camera_position[0],
                      y=weighted_camera_position[1],
                      z=weighted_camera_position[2],
                      roll=weighted_euler_angles[0],
                      pitch=weighted_euler_angles[1],
                      yaw=weighted_euler_angles[2])


    def __get_camera_pose(self, tag_world_corners, tag_image_corners):

        success, rvec, tvec = cv2.solvePnP(tag_world_corners, 
                                           tag_image_corners, 
                                           self.camera_matrix, 
                                           self.dist_coeffs)

        if not success:
            raise Exception("SolvePnP failed to find a solution.")
        
        rotation_matrix, _ = cv2.Rodrigues(rvec)
        
        rotation_matrix_inv = rotation_matrix.T
        
        camera_position = -rotation_matrix_inv @ tvec
        
        def rotation_matrix_to_euler_angles(R):
            sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
            singular = sy < 1e-6

            if not singular:
                theta = np.arctan2(R[2, 1], R[2, 2]) + np.pi/2
                psi = np.arctan2(-R[2, 0], sy)
                phi = np.arctan2(R[1, 0], R[0, 0]) + np.pi/2
            else:
                theta = np.arctan2(-R[1, 2], R[1, 1]) + np.pi/2
                psi = np.arctan2(-R[2, 0], sy)
                phi =  np.pi/2

            return np.array([psi, theta, phi])

        euler_angles = rotation_matrix_to_euler_angles(rotation_matrix_inv)
        
        camera_position = camera_position.flatten()

        return camera_position, euler_angles


    def __get_tag_world_corners(self, tag_pose):

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

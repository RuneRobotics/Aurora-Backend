from scipy.spatial.transform import Rotation as R
from capture.camera import Camera, Pose3D
from utils.json_utils import load_field
import pyapriltags as apriltag
from utils import constants
import numpy as np
import logging
import cv2


class AprilTagDetector:
    """
    Detects AprilTags and calculates camera poses based on detected tags.

    Attributes:
        camera (Camera): The camera instance associated with the detector.
        field_data (dict): Data about the field including tag poses.
        camera_matrix (np.ndarray): Intrinsic camera matrix.
        dist_coeffs (np.ndarray): Camera distortion coefficients.
    """

    def __init__(self, season: int, camera: Camera, families: str = 'tag36h11'):
        """
        Initialize the AprilTag detector.

        Args:
            season (int): Season identifier used to load field data.
            camera (Camera): Camera instance.
            families (str): AprilTag families to detect (default: 'tag36h11').
        """
        self.__detector = apriltag.Detector(families=families)
        self.camera = camera
        self.camera_matrix = camera.matrix
        self.dist_coeffs = camera.dist_coeffs
        self.field_data = load_field(season)

    def __detect(self, frame: np.ndarray) -> list:
        """
        Detect AprilTags in a frame.

        Args:
            frame (np.ndarray): The input video frame.

        Returns:
            list: Detected AprilTags.
        """
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.__detector.detect(gray_frame)

    def get_camera_and_tags_data(self, frame: np.ndarray) -> None:
        """
        Process a frame to detect tags and compute camera pose.

        Args:
            frame (np.ndarray): The input video frame.
        """
        detected_apriltags = []
        camera_poses = []

        detections = self.__detect(frame)

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
                camera_position, euler_angles = self.__get_camera_pose(tag_world_corners, tag_image_corners)
            except Exception as e:
                logging.error(f"Error: {e}. Exception during solvePnP.")
                continue

            corners_int = np.array(tag.corners, dtype=np.int32)
            frame = cv2.polylines(
                frame,
                [corners_int.reshape((-1, 1, 2))],
                isClosed=True,
                color=constants.PURPLE,
                thickness=6,
            )

            detected_apriltags.append(tag_id)
            camera_poses.append((camera_position, euler_angles, 1))  # Score placeholder: 1

        camera_position = self.__get_weighted_camera_pose(camera_poses)
        self.camera.detected_apriltags = detected_apriltags
        self.camera.field_pose = camera_position
        robot_pose = self.camera.get_robot_pose()
        self.camera.add_pose_to_queue(robot_pose)

        return robot_pose

    def __get_weighted_camera_pose(self, camera_positions: list) -> Pose3D | None:
        """
        Calculate the weighted average of camera poses based on tag scores.

        Args:
            camera_positions (list): List of camera positions with scores.

        Returns:
            Pose3D | None: Weighted average camera pose, or None if no valid poses.
        """
        total_scores = sum(position[2] for position in camera_positions)
        if total_scores == 0: # or not trusting the camera (tags too far / unclear / ...)
            return None

        weighted_camera_position = np.zeros(3)
        weighted_euler_angles = np.zeros(3)

        for position in camera_positions:
            camera_position, euler_angles, score = position
            weight = score / total_scores
            weighted_camera_position += np.array(camera_position) * weight
            weighted_euler_angles += np.array(euler_angles) * weight

        return Pose3D(
            x=weighted_camera_position[0],
            y=weighted_camera_position[1],
            z=weighted_camera_position[2],
            roll=weighted_euler_angles[0],
            pitch=weighted_euler_angles[1],
            yaw=weighted_euler_angles[2],
        )

    def __get_camera_pose(self, tag_world_corners: np.ndarray, tag_image_corners: np.ndarray) -> tuple:
        """
        SolvePnP to estimate the camera pose based on tag corners.

        Args:
            tag_world_corners (np.ndarray): World coordinates of the tag corners.
            tag_image_corners (np.ndarray): Image coordinates of the tag corners.

        Returns:
            tuple: Camera position and Euler angles.
        """
        success, rvec, tvec = cv2.solvePnP(tag_world_corners, tag_image_corners, self.camera_matrix, self.dist_coeffs)

        if not success:
            raise Exception("SolvePnP failed to find a solution.")

        rotation_matrix, _ = cv2.Rodrigues(rvec)
        rotation_matrix_inv = rotation_matrix.T
        camera_position = -rotation_matrix_inv @ tvec

        def rotation_matrix_to_euler_angles(R: np.ndarray) -> np.ndarray:
            sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
            singular = sy < 1e-6
            if not singular:
                theta = np.arctan2(R[2, 1], R[2, 2]) + np.pi / 2
                psi = np.arctan2(-R[2, 0], sy)
                phi = np.arctan2(R[1, 0], R[0, 0]) + np.pi / 2
            else:
                theta = np.arctan2(-R[1, 2], R[1, 1]) + np.pi / 2
                psi = np.arctan2(-R[2, 0], sy)
                phi = np.pi / 2
            return np.array([psi, theta, phi])

        euler_angles = rotation_matrix_to_euler_angles(rotation_matrix_inv)
        return camera_position.flatten(), euler_angles

    def __get_tag_world_corners(self, tag_pose: dict) -> np.ndarray:
        """
        Compute world coordinates of tag corners from the field data.

        Args:
            tag_pose (dict): Tag pose from field data.

        Returns:
            np.ndarray: World coordinates of the tag corners.
        """
        tag_half_size = constants.TAG_HALF_SIZE
        tag_translation = np.array(
            [
                tag_pose["translation"]["x"],
                tag_pose["translation"]["y"],
                tag_pose["translation"]["z"],
            ]
        )

        tag_quaternion = tag_pose["rotation"]["quaternion"]
        w, x, y, z = tag_quaternion["W"], tag_quaternion["X"], tag_quaternion["Y"], tag_quaternion["Z"]
        rotation = R.from_quat([x, y, z, w])

        tag_corners_local = np.array(
            [
                [0, -tag_half_size, -tag_half_size],
                [0, tag_half_size, -tag_half_size],
                [0, tag_half_size, tag_half_size],
                [0, -tag_half_size, tag_half_size],
            ]
        )

        tag_corners_world = rotation.apply(tag_corners_local) + tag_translation
        return tag_corners_world.astype(np.float64)

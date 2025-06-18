from scipy.spatial.transform import Rotation as R
from utils import constants
from queue import Queue
import numpy as np
from utils.pose3d import Pose3D
from detection.apriltag_detector import AprilTagDetector
import os
import globals
import json
import cv2

class Camera:
    """
    Represents a camera with intrinsic parameters, pose, and functionality for robot pose estimation.

    Attributes:
        id (int): Identifier for the camera.
        pose_on_robot (Pose3D): Pose of the camera relative to the robot.
        matrix (np.ndarray): Camera matrix containing intrinsic parameters.
        dist_coeffs (np.ndarray): Distortion coefficients for the camera.
        field_pose (Pose3D | None): Pose of the camera in the field coordinate system.
        frame (np.ndarray | None): Current frame captured by the camera.
    """

    def __init__(
        self,
        id: int
    ):
        
        self.id = id

        self.pose_on_robot = Pose3D()
        self.field_pose: Pose3D | None = None

        self.matrix = np.array([[600, 0, 320], [0, 600, 240], [0, 0, 1]], dtype=np.float32)
        self.dist_coeffs = np.zeros((4, 1))
        self.robot_pose_queue: Queue[Pose3D] = Queue(maxsize=constants.QUEUE_SIZE)

        self.apriltag_detector = None
        self.frame: np.ndarray | None = None
        self.display_frame: np.ndarray | None = None
        self.detected_apriltags: list = []
        
        self.__update_camera()

    def __update_camera(self):

        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, 'cameras_settings.json')
        with open(json_path) as f:
            cameras_settings = json.load(f)

        camera_dict = cameras_settings[self.id]

        self.settings = camera_dict["settings"]
        self.lighting = camera_dict["lighting"]
        self.calibration = camera_dict["calibration"]
        self.matrix = camera_dict["matrix"]
        self.dist_coeffs = camera_dict["distortion"]

        try:
            self.pose_on_robot = Pose3D(
                x=self.settings["x"],
                y=self.settings["y"],
                z=self.settings["z"],
                roll=self.settings["roll"],
                pitch=self.settings["pitch"],
                yaw=self.settings["yaw"]
            )
        except Exception:
            # settings error for camera
            pass

        self.apriltag_detector = AprilTagDetector(matrix=self.matrix, dist_coeffs=self.dist_coeffs, families='tag36h11', season=constants.REEFSCAPE)

    def get_robot_pose(self) -> Pose3D | None:
        """
        Calculate the robot pose based on the field and camera poses.

        Returns:
            Pose3D | None: The calculated robot pose, or None if field pose is unavailable.
        """
        if not isinstance(self.field_pose, Pose3D):
            return None

        camera_field_euler_angles = [self.field_pose.yaw, self.field_pose.pitch, self.field_pose.roll]
        camera_robot_euler_angles = [self.pose_on_robot.yaw, self.pose_on_robot.pitch, self.pose_on_robot.roll]

        def euler_to_mat(euler_angles: list[float]) -> np.ndarray:
            return R.from_euler("zyx", euler_angles).as_matrix()

        R_robot_to_camera = euler_to_mat(camera_robot_euler_angles)
        t_robot_to_camera = np.array([self.pose_on_robot.x, self.pose_on_robot.y, self.pose_on_robot.z])
        T_robot_to_camera = np.eye(4)
        T_robot_to_camera[:3, :3] = R_robot_to_camera
        T_robot_to_camera[:3, 3] = t_robot_to_camera

        R_field_to_camera = euler_to_mat(camera_field_euler_angles)
        t_field_to_camera = np.array([self.field_pose.x, self.field_pose.y, self.field_pose.z])
        T_field_to_camera = np.eye(4)
        T_field_to_camera[:3, :3] = R_field_to_camera
        T_field_to_camera[:3, 3] = t_field_to_camera

        T_robot_to_camera_inv = np.eye(4)
        T_robot_to_camera_inv[:3, :3] = R_robot_to_camera.T
        T_robot_to_camera_inv[:3, 3] = -R_robot_to_camera.T @ t_robot_to_camera

        T_field_to_robot = T_field_to_camera @ T_robot_to_camera_inv

        x, y, z = T_field_to_robot[:3, 3]
        robot_orientation = R.from_matrix(T_field_to_robot[:3, :3])
        yaw, pitch, roll = robot_orientation.as_euler('zyx', degrees=False)

        return Pose3D(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw)

    def add_pose_to_queue(self, pose: Pose3D) -> None:
        """
        Add a new pose to the robot pose queue.

        Args:
            pose (Pose3D): The pose to be added.
        """
        if self.robot_pose_queue.full():
            _ = self.robot_pose_queue.get()
        self.robot_pose_queue.put(pose)

    def run_detection(self):
        detected_apriltags, camera_position = self.apriltag_detector.get_detection_data(frame=self.display_frame)
        self.detected_apriltags = detected_apriltags
        self.field_pose = camera_position
        self.add_pose_to_queue(self.get_robot_pose())

    def run_stream(self):
        pass
    
    def run_settings(self):
        try:
            with globals.SETTINGS_LOCK:
                if globals.SETTINGS_CHANGED == True:
                    self.__update_camera()
                    globals.SETTINGS_CHANGED = False
                    print("settings changed!")
        except Exception as e:
            print(e)

    def run_lighting(self):
        pass

    def run_calibration(self):
        rows = self.calibration["rows"] - 1
        columns = self.calibration["columns"] - 1
        chessboard_size = (columns, rows)
        gray = cv2.cvtColor(self.display_frame, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
        if found:
            cv2.drawChessboardCorners(self.display_frame, chessboard_size, corners, found)

        try:
            with globals.SETTINGS_LOCK:
                if globals.SETTINGS_CHANGED == True:
                    self.__update_camera()
                    globals.SETTINGS_CHANGED = False
                    print("calibration changed!")
        except Exception as e:
            print(e)
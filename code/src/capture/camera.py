from scipy.spatial.transform import Rotation as R
from utils import constants
from queue import Queue
import numpy as np
from utils.pose3d import Pose3D
from detection.apriltag_detector import AprilTagDetector
from capture.calibration_utils import run_directory_calibration
import os
from globals import SEASON
import json

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
        try:
            self.matrix = self.calibration["matrix"]
            self.dist_coeffs = self.calibration["dist_coeffs"]
        except Exception:
            # calibration error for camera
            pass

        self.apriltag_detector = AprilTagDetector(matrix=self.matrix, dist_coeffs=self.dist_coeffs, families='tag36h11', season=SEASON)

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
        detected_apriltags, camera_position = self.apriltag_detector.get_detection_data(frame=self.frame)
        self.detected_apriltags = detected_apriltags
        self.field_pose = camera_position
        self.add_pose_to_queue(self.get_robot_pose())

    def run_stream(self):
        pass
    
    def run_settings(self):
        GLOBAL_FLAG = True
        if GLOBAL_FLAG:
            #change stuff
            GLOBAL_FLAG = False

        # change the settings file for this camera, and change this instance of the camera
        # the change happnes only if a global flag is turned on - meaning there was a change, and then we change it to false
        self.__update_camera()

    def run_lighting(self):
        pass

    def run_calibration(self):
        pass
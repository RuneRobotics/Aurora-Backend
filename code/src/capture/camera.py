from scipy.spatial.transform import Rotation as R
from utils import constants
from queue import Queue
import numpy as np


class Pose3D:
    """
    Represents a 3D pose with position and orientation.

    Attributes:
        x (float): X-coordinate of the pose.
        y (float): Y-coordinate of the pose.
        z (float): Z-coordinate of the pose.
        roll (float): Rotation around the X-axis in radians.
        pitch (float): Rotation around the Y-axis in radians.
        yaw (float): Rotation around the Z-axis in radians.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, roll: float = 0.0, pitch: float = 0.0, yaw: float = 0.0):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def equals(self, other: object) -> bool:
        """
        Checks if two Pose3D objects are equal.

        Two Pose3D objects are considered equal if their position (x, y, z)
        and orientation (roll, pitch, yaw) values are numerically close within
        a small tolerance.

        Args:
            other (Pose3D): The other Pose3D instance to compare.

        Returns:
            bool: True if the poses are approximately equal, False otherwise.
        """
        if not isinstance(other, Pose3D):
            return False
        return np.allclose(
            [self.x, self.y, self.z, self.roll, self.pitch, self.yaw],
            [other.x, other.y, other.z, other.roll, other.pitch, other.yaw]
        )
    
    def to_string(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}, roll: {self.roll}, pitch: {self.pitch}, yaw: {self.yaw}"


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
        id: int,
        pose_on_robot: Pose3D = Pose3D(),
        matrix: np.ndarray = np.array([[600, 0, 320], [0, 600, 240], [0, 0, 1]], dtype=np.float32),
        dist_coeffs: np.ndarray = np.zeros((4, 1))
    ):
        self.robot_pose_queue: Queue[Pose3D] = Queue(maxsize=constants.QUEUE_SIZE)
        self.detected_apriltags: list = []
        self.id = id
        self.pose_on_robot = pose_on_robot
        self.field_pose: Pose3D | None = None
        self.matrix = matrix
        self.dist_coeffs = dist_coeffs
        self.frame: np.ndarray | None = None

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

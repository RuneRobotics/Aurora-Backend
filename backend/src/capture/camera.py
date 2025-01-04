import numpy as np
from queue import Queue
from utils import constants
from scipy.spatial.transform import Rotation as R

class Pose3D:
    def __init__(self, x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

class Camera:
    def __init__(self,
                 id,
                 pose_on_robot: Pose3D=Pose3D(), 
                 matrix = np.array([[600, 0, 320],  # fx, 0, cx
                                    [0, 600, 240],  # 0, fy, cy
                                    [0, 0, 1]], dtype=np.float32),
                dist_coeffs = np.zeros((4, 1))):
        
        self.robot_pose_queue = Queue(maxsize=constants.QUEUE_SIZE)
        self.deteceted_apriltags = []
        self.id = id
        self.pose_on_robot = pose_on_robot
        self.field_pose = None
        self.matrix = matrix
        self.dist_coeffs = dist_coeffs
        self.frame = None

    def get_robot_pose(self):
        

        if not isinstance(self.field_pose, Pose3D):
            return None

        camera_field_euler_angles = [self.field_pose.yaw, 
                                     self.field_pose.pitch, 
                                     self.field_pose.roll]
        
        camera_robot_euler_angles = [self.pose_on_robot.yaw, 
                                     self.pose_on_robot.pitch, 
                                     self.pose_on_robot.roll]
        
        camera_field_position = np.array([self.field_pose.x, 
                                          self.field_pose.y, 
                                          self.field_pose.z])
        
        camera_robot_position = np.array([self.pose_on_robot.x, 
                                          self.pose_on_robot.y, 
                                          self.pose_on_robot.z])

        def euler_to_mat(euler_angles: list):
            return R.from_euler("zyx", euler_angles).as_matrix()
        
        field_to_camera_mat = euler_to_mat(camera_field_euler_angles)
        robot_to_camera_mat = euler_to_mat(camera_robot_euler_angles)

        field_to_robot_rotation = np.linalg.inv(robot_to_camera_mat) @ field_to_camera_mat
        #field_to_robot_translation = camera_field_position - np.linalg.inv(field_to_camera_mat) @ robot_to_camera_mat @ camera_robot_position

        field_to_robot_translation = (
        camera_field_position 
        - field_to_camera_mat @ camera_robot_position
        )

        print("camera field position", self.field_pose.x, self.field_pose.y)

        x, y, z = field_to_robot_translation
        yaw, pitch, roll = R.from_matrix(field_to_robot_rotation).as_euler("zyx")

        print("robot field position", x, y)
        
        return Pose3D(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw)


    def add_pose_to_queue(self, pose):

        if self.robot_pose_queue.full():
            _ = self.robot_pose_queue.get()
        
        self.robot_pose_queue.put(pose)

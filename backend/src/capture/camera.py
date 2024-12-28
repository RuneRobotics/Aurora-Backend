import numpy as np
from queue import Queue
from utils import constants

class Pose3D:
    def __init__(self, x=0, y=0, z=0, roll=0, pitch=0, yaw=0):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

class Camera:
    def __init__(self,
                 id,
                 position_on_robot: Pose3D=Pose3D(), 
                 matrix = np.array([[600, 0, 320],  # fx, 0, cx
                                    [0, 600, 240],  # 0, fy, cy
                                    [0, 0, 1]], dtype=np.float32),
                dist_coeffs = np.zeros((4, 1))):
        
        self.robot_pose_queue = Queue(maxsize=constants.QUEUE_SIZE)
        self.deteceted_apriltags = []
        self.id = id
        self.position_on_robot = position_on_robot
        self.field_position = None
        self.matrix = matrix
        self.dist_coeffs = dist_coeffs
        self.frame = None

    def get_robot_pose(self):
        if self.field_position is None:
            return None
        
        # Extract field position of the camera
        cam_x = self.field_position.x
        cam_y = self.field_position.y
        cam_z = self.field_position.z
        cam_roll = self.field_position.roll
        cam_pitch = self.field_position.pitch
        cam_yaw = self.field_position.yaw

        # Extract the camera's position on the robot
        robot_rel_x = self.position_on_robot.x
        robot_rel_y = self.position_on_robot.y
        robot_rel_z = self.position_on_robot.z
        robot_rel_roll = self.position_on_robot.roll
        robot_rel_pitch = self.position_on_robot.pitch
        robot_rel_yaw = self.position_on_robot.yaw

        robot_x = cam_x - robot_rel_x
        robot_y = cam_y - robot_rel_y
        robot_z = cam_z - robot_rel_z
        robot_roll = cam_roll - robot_rel_roll
        robot_pitch = cam_pitch - robot_rel_pitch
        robot_yaw = cam_yaw - robot_rel_yaw

        # Return the calculated robot position as a Pose3D object
        return Pose3D(robot_x, robot_y, robot_z, robot_roll, robot_pitch, robot_yaw)

        # NEEDS TO BE IMPLEMENTED
        # this return value is just for now
        return self.field_position

    def add_pose_to_queue(self, pose):

        if self.robot_pose_queue.full():
            _ = self.robot_pose_queue.get()
        
        self.robot_pose_queue.put(pose)

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
        # NEEDS TO BE IMPLEMENTED
        return self.field_position

    def add_pose_to_queue(self, pose):

        if self.robot_pose_queue.full():
            _ = self.robot_pose_queue.get()
        
        self.robot_pose_queue.put(pose)

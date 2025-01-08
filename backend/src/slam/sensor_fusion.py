from queue import Queue
from typing import List
from pathlib import Path
from utils import constants
from capture.camera import Camera, Pose3D
from utils.output_formats import pose3d_format, data_format
from slam.kalman_filter import KalmanFilter
import time
from math import radians, degrees, pi
import numpy as np
from utils.json_utils import dict_to_json


def average_pose3d(pose_queue):
    total_x = total_y = total_z = 0.0
    total_roll = total_pitch = total_yaw = 0.0
    count = 0

    # Create a copy of the queue to iterate without removing elements
    queue_list = list(pose_queue.queue)

    for pose in queue_list:
        total_x += pose.x
        total_y += pose.y
        total_z += pose.z
        total_roll += pose.roll
        total_pitch += pose.pitch
        total_yaw += pose.yaw
        count += 1

    if count == 0:
        return Pose3D()  # Return a default Pose3D if queue is empty

    avg_pose = Pose3D(
        x=total_x / count,
        y=total_y / count,
        z=total_z / count,
        roll=total_roll / count,
        pitch=total_pitch / count,
        yaw=total_yaw / count
    )

    return avg_pose

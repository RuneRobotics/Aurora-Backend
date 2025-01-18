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
    total_roll_sin = total_roll_cos = 0.0
    total_pitch_sin = total_pitch_cos = 0.0
    total_yaw_sin = total_yaw_cos = 0.0
    count = 0

    # Create a copy of the queue to iterate without removing elements
    queue_list = list(pose_queue.queue)

    for pose in queue_list:
        total_x += pose.x
        total_y += pose.y
        total_z += pose.z

        total_roll_sin += np.sin(pose.roll)
        total_roll_cos += np.cos(pose.roll)

        total_pitch_sin += np.sin(pose.pitch)
        total_pitch_cos += np.cos(pose.pitch)

        total_yaw_sin += np.sin(pose.yaw)
        total_yaw_cos += np.cos(pose.yaw)

        count += 1

    if count == 0:
        return Pose3D()  # Return a default Pose3D if queue is empty

    avg_x = total_x / count
    avg_y = total_y / count
    avg_z = total_z / count

    avg_roll = np.arctan2(total_roll_sin / count, total_roll_cos / count)
    avg_pitch = np.arctan2(total_pitch_sin / count, total_pitch_cos / count)
    avg_yaw = np.arctan2(total_yaw_sin / count, total_yaw_cos / count)

    avg_pose = Pose3D(
        x=avg_x,
        y=avg_y,
        z=avg_z,
        roll=avg_roll,
        pitch=avg_pitch,
        yaw=avg_yaw
    )

    return avg_pose

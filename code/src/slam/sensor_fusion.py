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
        if isinstance(pose, Pose3D):
            if not pose.equals(Pose3D()): # change later to a "default pose"
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
            print(f"pose {count}: {pose.to_string()}")
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

    print(f"avg pose: {avg_pose.to_string()}")
    return avg_pose


def ema_pose3d(old_state: Pose3D, reading: Pose3D, alpha: float) -> Pose3D:
    """
    Perform Exponential Moving Average (EMA) for a Pose3D object.

    Parameters:
        old_state (Pose3D): The previous state.
        reading (Pose3D): The new reading to incorporate.
        alpha (float): The smoothing factor (0 < alpha <= 1).

    Returns:
        Pose3D: The updated state after applying EMA.
    """
    # Linear components (x, y, z) use standard EMA
    new_x = alpha * reading.x + (1 - alpha) * old_state.x
    new_y = alpha * reading.y + (1 - alpha) * old_state.y
    new_z = alpha * reading.z + (1 - alpha) * old_state.z

    # Angular components (roll, pitch, yaw) use sine and cosine for EMA
    roll_sin = alpha * np.sin(reading.roll) + (1 - alpha) * np.sin(old_state.roll)
    roll_cos = alpha * np.cos(reading.roll) + (1 - alpha) * np.cos(old_state.roll)
    new_roll = np.arctan2(roll_sin, roll_cos)

    pitch_sin = alpha * np.sin(reading.pitch) + (1 - alpha) * np.sin(old_state.pitch)
    pitch_cos = alpha * np.cos(reading.pitch) + (1 - alpha) * np.cos(old_state.pitch)
    new_pitch = np.arctan2(pitch_sin, pitch_cos)

    yaw_sin = alpha * np.sin(reading.yaw) + (1 - alpha) * np.sin(old_state.yaw)
    yaw_cos = alpha * np.cos(reading.yaw) + (1 - alpha) * np.cos(old_state.yaw)
    new_yaw = np.arctan2(yaw_sin, yaw_cos)

    # Return the updated Pose3D
    return Pose3D(
        x=new_x,
        y=new_y,
        z=new_z,
        roll=new_roll,
        pitch=new_pitch,
        yaw=new_yaw
    )

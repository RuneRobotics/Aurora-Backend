from queue import Queue
from typing import List
from pathlib import Path
from utils import constants
from capture.camera import Camera, Pose3D
from utils.data_formats import pose3d_format
from slam.kalman_filter import KalmanFilter
import time
from math import radians, degrees, pi
import numpy as np

def fuse_data(cameras: List[Camera], fused_output_file: Path):

    num_cameras = len(cameras)
    kf = KalmanFilter(process_noise=0.01, measurement_noise=0.1, num_cameras=num_cameras)

    while(True):

        queues = []

        for camera in cameras:
            queues.append(camera.robot_pose_queue)

        # Collect the latest measurements from all camera queues
        measurements = []
        for queue in queues:
            if not queue.empty():
                pose = queue.get()
                # Convert Pose3D to a measurement vector
                measurements.append(np.array([
                    [pose.x],
                    [pose.y],
                    [pose.z],
                    [radians(pose.roll)],
                    [radians(pose.pitch)],
                    [radians(pose.yaw)],
                ]))
            else:
                # If a queue is empty, use a placeholder (e.g., last known state or zeros)
                measurements.append(np.zeros((6, 1)))

        # Kalman filter prediction and update
        kf.predict()
        kf.update(measurements)

        # Get fused pose and write to the output file
        fused_pose = kf.get_state()

        print(pose3d_format(fused_pose))

        time.sleep(constants.UPDATE_INTERVAL*25)
